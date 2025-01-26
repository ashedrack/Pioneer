import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

import numpy as np
import pytz
import tensorflow as tf
from dateutil import parser


class ResourcePredictor:
    def __init__(self):
        self.model = None
        self._metrics_store = defaultdict(list)
        self.logger = logging.getLogger(__name__)

    def build_model(self, input_shape: tuple) -> None:
        """Build and compile the LSTM model for resource usage prediction."""
        self.model = tf.keras.Sequential(
            [
                tf.keras.layers.LSTM(
                    64, input_shape=input_shape, return_sequences=True
                ),
                tf.keras.layers.LSTM(32),
                tf.keras.layers.Dense(24),  # Predict next 24 hours
                tf.keras.layers.Activation("sigmoid"),
            ]
        )

        self.model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50) -> Dict[str, Any]:
        """Train the model on historical resource usage data."""
        if self.model is None:
            self.build_model(input_shape=(X.shape[1], X.shape[2]))

        history = self.model.fit(
            X,
            y,
            epochs=epochs,
            validation_split=0.2,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor="val_loss", patience=5, restore_best_weights=True
                )
            ],
        )
        return history.history

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict resource usage for the next 24 hours."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        predictions = self.model.predict(X)
        return predictions

    def evaluate_prediction(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ) -> Dict[str, float]:
        """Evaluate prediction accuracy."""
        mse = np.mean((y_true - y_pred) ** 2)
        mae = np.mean(np.abs(y_true - y_pred))

        return {"mse": float(mse), "mae": float(mae), "rmse": float(np.sqrt(mse))}

    def store_metrics(
        self, resource_id: str, timestamp: str, metrics: Dict[str, float]
    ) -> None:
        """Store resource metrics."""
        try:
            self._metrics_store[resource_id].append(
                {"timestamp": timestamp, "metrics": metrics}
            )
            self.logger.info(
                f"Stored metrics for resource {resource_id} at {timestamp}"
            )
        except Exception as e:
            self.logger.error(f"Failed to store metrics: {str(e)}")
            raise

    def get_historical_metrics(
        self, resource_id: str, start_time: str, end_time: str
    ) -> List[Dict[str, Any]]:
        """Get historical metrics for a resource."""
        try:
            metrics = self._metrics_store.get(resource_id, [])

            # Convert timestamps to UTC for comparison
            def parse_timestamp(ts: str) -> datetime:
                dt = parser.parse(ts)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=pytz.UTC)
                return dt.astimezone(pytz.UTC)

            start = parse_timestamp(start_time)
            end = parse_timestamp(end_time)

            filtered_metrics = []
            for metric in metrics:
                timestamp = parse_timestamp(metric["timestamp"])
                if start <= timestamp <= end:
                    filtered_metrics.append(metric)

            return filtered_metrics
        except Exception as e:
            self.logger.error(f"Failed to get historical metrics: {str(e)}")
            raise

    def predict_usage(self, resource_id: str, hours: int = 24) -> Dict[str, Any]:
        """Predict future resource usage."""
        try:
            # Mock prediction for development
            now = datetime.now(pytz.UTC)
            return {
                "cpu_usage": [
                    {"timestamp": (now + timedelta(hours=i)).isoformat(), "value": 50.0}
                    for i in range(hours)
                ],
                "memory_usage": [
                    {"timestamp": (now + timedelta(hours=i)).isoformat(), "value": 40.0}
                    for i in range(hours)
                ],
            }
        except Exception as e:
            self.logger.error(f"Failed to predict usage: {str(e)}")
            raise
