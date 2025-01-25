import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List, Dict, Any
import logging
from .base import MetricBackend
from ..agent import Metric

class TimeSeriesBackend(MetricBackend):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = influxdb_client.InfluxDBClient(
            url=config['url'],
            token=config['token'],
            org=config['org']
        )
        self.bucket = config['bucket']
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.logger = logging.getLogger(__name__)

    def send_metrics(self, metrics: List[Metric]):
        try:
            points = []
            for metric in metrics:
                point = influxdb_client.Point(metric.name)\
                    .time(int(metric.timestamp * 1e9))\
                    .field("value", metric.value)
                
                # Add tags
                for key, value in metric.tags.items():
                    point = point.tag(key, value)
                
                points.append(point)
            
            self.write_api.write(bucket=self.bucket, record=points)
        except Exception as e:
            self.logger.error(f"Error sending metrics to InfluxDB: {e}")

    def health_check(self) -> bool:
        try:
            self.client.ping()
            return True
        except Exception:
            return False
