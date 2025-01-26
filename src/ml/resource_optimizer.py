import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

import boto3
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


class ResourceOptimizer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.logger = logging.getLogger(__name__)
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("cloud_pioneer_metrics")
        self.feature_columns = [
            "cpu_utilization",
            "memory_utilization",
            "network_in",
            "network_out",
        ]

    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for the model."""
        features = []

        # Time-based features
        df["hour"] = df.index.hour
        df["day_of_week"] = df.index.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        # Rolling statistics
        df["rolling_mean"] = df["value"].rolling(window=24).mean()
        df["rolling_std"] = df["value"].rolling(window=24).std()

        # Lag features
        for lag in [1, 24, 168]:  # 1 hour, 1 day, 1 week
            df[f"lag_{lag}"] = df["value"].shift(lag)

        feature_columns = [
            "hour",
            "day_of_week",
            "is_weekend",
            "rolling_mean",
            "rolling_std",
            "lag_1",
            "lag_24",
            "lag_168",
        ]

        return df[feature_columns].fillna(method="bfill")

    def train(self, historical_data: pd.DataFrame):
        """Train the resource optimization model."""
        try:
            features = self.prepare_features(historical_data)
            target = historical_data["value"]

            # Remove rows with NaN values
            valid_idx = ~features.isna().any(axis=1) & ~target.isna()
            features = features[valid_idx]
            target = target[valid_idx]

            # Scale features
            scaled_features = self.scaler.fit_transform(features)

            # Train model
            self.model = RandomForestRegressor(
                n_estimators=100, max_depth=10, random_state=42
            )
            self.model.fit(scaled_features, target)

            # Save model and scaler
            joblib.dump(self.model, "models/resource_optimizer.joblib")
            joblib.dump(self.scaler, "models/scaler.joblib")

        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            raise

    def predict_utilization(
        self, current_data: pd.DataFrame, horizon_hours: int = 24
    ) -> Dict[str, Any]:
        """Predict resource utilization for the next n hours."""
        try:
            if self.model is None:
                self.model = joblib.load("models/resource_optimizer.joblib")
                self.scaler = joblib.load("models/scaler.joblib")

            predictions = []
            last_data = current_data.copy()

            for i in range(horizon_hours):
                features = self.prepare_features(last_data)
                scaled_features = self.scaler.transform(features.iloc[[-1]])
                pred = self.model.predict(scaled_features)[0]

                timestamp = last_data.index[-1] + timedelta(hours=1)
                predictions.append({"timestamp": timestamp, "predicted_value": pred})

                # Add prediction to historical data for next iteration
                new_row = pd.DataFrame({"value": [pred]}, index=[timestamp])
                last_data = pd.concat([last_data, new_row])

            return {
                "predictions": predictions,
                "recommended_actions": self._generate_recommendations(predictions),
            }

        except Exception as e:
            self.logger.error(f"Error making predictions: {e}")
            raise

    def _generate_recommendations(self, predictions: List[Dict]) -> List[Dict]:
        """Generate resource optimization recommendations."""
        recommendations = []
        threshold_low = self.config.get("utilization_threshold_low", 20)
        threshold_high = self.config.get("utilization_threshold_high", 80)

        # Group consecutive periods of low/high utilization
        current_period = None
        for pred in predictions:
            value = pred["predicted_value"]

            if value < threshold_low:
                if current_period is None or current_period["type"] != "low":
                    if current_period:
                        recommendations.append(current_period)
                    current_period = {
                        "type": "low",
                        "start_time": pred["timestamp"],
                        "end_time": pred["timestamp"],
                        "avg_value": value,
                    }
                else:
                    current_period["end_time"] = pred["timestamp"]
                    current_period["avg_value"] = (
                        current_period["avg_value"] + value
                    ) / 2

            elif value > threshold_high:
                if current_period is None or current_period["type"] != "high":
                    if current_period:
                        recommendations.append(current_period)
                    current_period = {
                        "type": "high",
                        "start_time": pred["timestamp"],
                        "end_time": pred["timestamp"],
                        "avg_value": value,
                    }
                else:
                    current_period["end_time"] = pred["timestamp"]
                    current_period["avg_value"] = (
                        current_period["avg_value"] + value
                    ) / 2

        if current_period:
            recommendations.append(current_period)

        # Convert recommendations to actions
        actions = []
        for rec in recommendations:
            if rec["type"] == "low":
                actions.append(
                    {
                        "action": "scale_down",
                        "start_time": rec["start_time"],
                        "end_time": rec["end_time"],
                        "reason": f"Low utilization predicted ({rec['avg_value']:.1f}%)",
                    }
                )
            else:
                actions.append(
                    {
                        "action": "scale_up",
                        "start_time": rec["start_time"],
                        "end_time": rec["end_time"],
                        "reason": f"High utilization predicted ({rec['avg_value']:.1f}%)",
                    }
                )

        return actions

    def get_historical_data(self, resource_id: str, days: int = 7) -> pd.DataFrame:
        """Get historical metrics data for a resource"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            response = self.table.query(
                KeyConditionExpression="resource_id = :rid AND timestamp BETWEEN :start AND :end",
                ExpressionAttributeValues={
                    ":rid": resource_id,
                    ":start": start_time.isoformat(),
                    ":end": end_time.isoformat(),
                },
            )

            if not response.get("Items"):
                return pd.DataFrame(columns=self.feature_columns)

            df = pd.DataFrame(response["Items"])
            return df[self.feature_columns].fillna(method="ffill")
        except Exception as e:
            print(f"Error getting historical data: {e}")
            return pd.DataFrame(columns=self.feature_columns)

    def predict_resource_usage(self, data: pd.DataFrame) -> List[Dict[str, float]]:
        """Predict future resource usage based on historical data"""
        try:
            # Simple moving average prediction for now
            window = min(24, len(data))
            predictions = []

            for col in self.feature_columns:
                if col in data.columns:
                    rolling_mean = (
                        data[col].rolling(window=window, min_periods=1).mean()
                    )
                    predictions.append(
                        {
                            "metric": col,
                            "prediction": float(rolling_mean.iloc[-1]),
                            "confidence": 0.8,  # Placeholder confidence score
                        }
                    )

            return predictions
        except Exception as e:
            print(f"Error predicting resource usage: {e}")
            return []

    def get_recommendations(self, resource_id: str) -> Dict[str, Any]:
        """Get resource optimization recommendations"""
        try:
            # Get historical data
            data = self.get_historical_data(resource_id)
            if data.empty:
                return {"status": "error", "message": "No historical data available"}

            # Get predictions
            predictions = self.predict_resource_usage(data)

            # Generate recommendations
            recommendations = []
            thresholds = {
                "cpu_utilization": {"low": 20, "high": 80},
                "memory_utilization": {"low": 30, "high": 85},
                "network_in": {"low": 1000000, "high": 100000000},  # 1MB/s to 100MB/s
                "network_out": {"low": 1000000, "high": 100000000},
            }

            for pred in predictions:
                metric = pred["metric"]
                value = pred["prediction"]

                if metric in thresholds:
                    if value < thresholds[metric]["low"]:
                        recommendations.append(
                            {
                                "metric": metric,
                                "current_value": value,
                                "recommendation": "downsize",
                                "reason": f'{metric} is consistently below {thresholds[metric]["low"]}',
                            }
                        )
                    elif value > thresholds[metric]["high"]:
                        recommendations.append(
                            {
                                "metric": metric,
                                "current_value": value,
                                "recommendation": "upsize",
                                "reason": f'{metric} is consistently above {thresholds[metric]["high"]}',
                            }
                        )

            return {
                "status": "success",
                "resource_id": resource_id,
                "predictions": predictions,
                "recommendations": recommendations,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
