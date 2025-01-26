"""Resource monitor module."""

import logging
from datetime import datetime
from typing import Any, Dict, List

from src.agent.collectors.resource_metrics import ResourceMetricsCollector
from src.automation.scheduler import ResourceScheduler
from src.ml.models.prediction import MetricsPredictor


class ResourceMonitor:
    """Monitors cloud resources and manages their optimization."""

    def __init__(
        self,
        metrics_collector: ResourceMetricsCollector = None,
        predictor: MetricsPredictor = None,
        scheduler: ResourceScheduler = None,
    ):
        """Initialize monitor with collectors and predictors."""
        self.metrics_collector = metrics_collector or ResourceMetricsCollector()
        self.predictor = predictor or MetricsPredictor()
        self.scheduler = scheduler or ResourceScheduler()
        self.logger = logging.getLogger(__name__)

    def collect_metrics(self, resource_id: str) -> Dict[str, Any]:
        """Collect metrics for a resource."""
        try:
            metrics = self.metrics_collector.collect_metrics(resource_id)
            metrics_data = {
                "resource_id": resource_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
            }

            # Store metrics
            self.predictor.store_metrics(metrics_data)

            return metrics_data
        except Exception as e:
            self.logger.error(f"Failed to collect metrics for {resource_id}: {str(e)}")
            raise

    def predict_usage(self, resource_id: str) -> Dict[str, Any]:
        """Predict resource usage."""
        try:
            metrics = self.collect_metrics(resource_id)
            return self.predictor.predict(metrics)
        except Exception as e:
            self.logger.error(f"Failed to predict usage for {resource_id}: {str(e)}")
            raise

    def get_recommendations(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get optimization recommendations."""
        try:
            return self.predictor.get_recommendations(resource_id)
        except Exception as e:
            self.logger.error(
                f"Failed to get recommendations for {resource_id}: {str(e)}"
            )
            raise

    def schedule_action(self, action: Dict[str, Any]) -> None:
        """Schedule a resource action."""
        try:
            self.scheduler.schedule_action(action)
        except Exception as e:
            self.logger.error(f"Failed to schedule action: {str(e)}")
            raise

    def get_scheduled_actions(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get scheduled actions for a resource."""
        try:
            return self.scheduler.get_scheduled_actions(resource_id)
        except Exception as e:
            self.logger.error(
                f"Failed to get scheduled actions for {resource_id}: {str(e)}"
            )
            raise
