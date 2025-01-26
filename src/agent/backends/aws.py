from typing import Any, Dict, List

import boto3

from ..agent import Metric
from .base import MetricBackend


class AWSBackend(MetricBackend):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.cloudwatch = boto3.client(
            "cloudwatch",
            region_name=config.get("region", "us-east-1"),
            aws_access_key_id=config.get("aws_access_key_id"),
            aws_secret_access_key=config.get("aws_secret_access_key"),
        )

    def send_metrics(self, metrics: List[Metric]):
        metric_data = []

        for metric in metrics:
            dimensions = [
                {"Name": key, "Value": value} for key, value in metric.tags.items()
            ]

            metric_data.append(
                {
                    "MetricName": metric.name,
                    "Value": metric.value,
                    "Timestamp": metric.timestamp,
                    "Dimensions": dimensions,
                    "Unit": "None",
                }
            )

            if len(metric_data) >= 20:  # CloudWatch limit
                self._send_batch(metric_data)
                metric_data = []

        if metric_data:
            self._send_batch(metric_data)

    def _send_batch(self, metric_data: List[Dict]):
        try:
            self.cloudwatch.put_metric_data(
                Namespace="CloudPioneer", MetricData=metric_data
            )
        except Exception as e:
            self.logger.error(f"Error sending metrics to CloudWatch: {e}")

    def health_check(self) -> bool:
        try:
            self.cloudwatch.list_metrics(Namespace="CloudPioneer", Limit=1)
            return True
        except Exception:
            return False
