"""Metrics prediction module."""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List

import boto3
import pandas as pd


class MetricsPredictor:
    """Predicts resource metrics based on historical data."""

    def __init__(self, dynamodb=None):
        """Initialize predictor with DynamoDB resource."""
        self.dynamodb = dynamodb or boto3.resource("dynamodb")
        self.metrics_table = self.dynamodb.Table("cloud_pioneer_metrics")
        self.logger = logging.getLogger(__name__)

    def store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store metrics in DynamoDB."""
        try:
            # Convert float values to Decimal for DynamoDB
            item = {
                "resource_id": metrics["resource_id"],
                "timestamp": metrics["timestamp"],
                "metrics": {k: Decimal(str(v)) for k, v in metrics["metrics"].items()},
            }

            self.metrics_table.put_item(Item=item)

        except Exception as e:
            self.logger.error(f"Failed to store metrics: {str(e)}")
            raise

    def predict(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Predict future metrics based on current metrics."""
        try:
            # Get historical metrics
            historical = self.get_historical_metrics(metrics["resource_id"])

            if historical.empty:
                return {"predictions": {}}

            # Simple prediction based on moving average
            predictions = {}
            for col in historical.columns:
                if col not in ["resource_id", "timestamp"]:
                    predictions[col] = float(historical[col].mean())

            return {"predictions": predictions}

        except Exception as e:
            self.logger.error(f"Failed to predict metrics: {str(e)}")
            raise

    def get_historical_metrics(self, resource_id: str) -> pd.DataFrame:
        """Get historical metrics for a resource."""
        try:
            # Query metrics from the last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)

            response = self.metrics_table.query(
                KeyConditionExpression="resource_id = :rid AND #ts BETWEEN :start AND :end",
                ExpressionAttributeNames={"#ts": "timestamp"},
                ExpressionAttributeValues={
                    ":rid": resource_id,
                    ":start": start_time.isoformat(),
                    ":end": end_time.isoformat(),
                },
            )

            if not response["Items"]:
                return pd.DataFrame()

            # Convert to DataFrame
            metrics = []
            for item in response["Items"]:
                metrics.append(
                    {
                        "resource_id": item["resource_id"],
                        "timestamp": item["timestamp"],
                        **{k: float(v) for k, v in item["metrics"].items()},
                    }
                )

            return pd.DataFrame(metrics)

        except Exception as e:
            self.logger.error(f"Failed to get historical metrics: {str(e)}")
            raise
