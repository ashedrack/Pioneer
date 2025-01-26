from datetime import datetime
from typing import Any, Dict, List

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import MetricsClient

from ..agent import Metric
from .base import MetricBackend


class AzureBackend(MetricBackend):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.credential = DefaultAzureCredential()
        self.metrics_client = MetricsClient(
            credential=self.credential,
            metrics_account_name=config["metrics_account_name"],
        )
        self.logger = logging.getLogger(__name__)

    def send_metrics(self, metrics: List[Metric]):
        try:
            metric_data = []
            for metric in metrics:
                metric_data.append(
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "time": datetime.fromtimestamp(metric.timestamp).isoformat(),
                        "dimensions": metric.tags,
                    }
                )

            if metric_data:
                self.metrics_client.submit_metrics(
                    rule_id=self.config["rule_id"], metrics=metric_data
                )
        except Exception as e:
            self.logger.error(f"Error sending metrics to Azure Monitor: {e}")

    def health_check(self) -> bool:
        try:
            # Attempt to list metric definitions
            self.metrics_client.list_metric_definitions()
            return True
        except Exception:
            return False
