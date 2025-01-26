import logging
from typing import Any, Dict, List

from google.api import label_pb2, metric_pb2
from google.cloud import monitoring_v3

from ..agent import Metric
from .base import MetricBackend


class GCPBackend(MetricBackend):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.project_name = config["project_name"]
        self.client = monitoring_v3.MetricServiceClient()
        self.project_path = f"projects/{self.project_name}"
        self.logger = logging.getLogger(__name__)

    def send_metrics(self, metrics: List[Metric]):
        try:
            for metric in metrics:
                series = monitoring_v3.TimeSeries()
                series.metric.type = f"custom.googleapis.com/{metric.name}"

                # Add labels (tags)
                for key, value in metric.tags.items():
                    series.metric.labels[key] = str(value)

                # Add resource
                series.resource.type = "global"

                # Create the data point
                point = monitoring_v3.Point()
                point.value.double_value = float(metric.value)
                point.interval.end_time.seconds = int(metric.timestamp)
                series.points = [point]

                # Write the time series data
                self.client.create_time_series(
                    request={"name": self.project_path, "time_series": [series]}
                )
        except Exception as e:
            self.logger.error(f"Error sending metrics to Google Cloud Monitoring: {e}")

    def health_check(self) -> bool:
        try:
            # Try to list metric descriptors
            self.client.list_metric_descriptors(name=self.project_path, page_size=1)
            return True
        except Exception:
            return False
