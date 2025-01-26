"""Resource optimizer module."""

import logging
from typing import Any, Dict, List

from src.ml.models.prediction import MetricsPredictor


class ResourceOptimizer:
    """Optimizes resource allocation based on metrics and predictions."""

    def __init__(self, predictor: MetricsPredictor = None):
        """Initialize optimizer with predictor."""
        self.predictor = predictor or MetricsPredictor()
        self.logger = logging.getLogger(__name__)

    def optimize_resource(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get optimization recommendations for a resource."""
        try:
            # Get current metrics and predictions
            metrics = self.predictor.get_historical_metrics(resource_id)
            predictions = self.predictor.predict({"resource_id": resource_id})

            # Generate recommendations
            recommendations = self.get_recommendations(metrics)

            return recommendations

        except Exception as e:
            self.logger.error(f"Failed to optimize resource {resource_id}: {str(e)}")
            raise

    def get_recommendations(self, metrics_df) -> List[Dict[str, Any]]:
        """Get recommendations from metrics DataFrame."""
        try:
            recommendations = []

            if not metrics_df.empty:
                # CPU recommendations
                if "cpu_utilization" in metrics_df:
                    cpu_util = float(metrics_df["cpu_utilization"].mean())
                    if cpu_util < 30:
                        recommendations.append(
                            {
                                "metric": "cpu",
                                "current_value": cpu_util,
                                "recommended_value": cpu_util * 0.5,
                                "recommendation": "Consider downsizing CPU allocation",
                            }
                        )
                    elif cpu_util > 80:
                        recommendations.append(
                            {
                                "metric": "cpu",
                                "current_value": cpu_util,
                                "recommended_value": cpu_util * 1.5,
                                "recommendation": "Consider increasing CPU allocation",
                            }
                        )

                # Memory recommendations
                if "memory_utilization" in metrics_df:
                    mem_util = float(metrics_df["memory_utilization"].mean())
                    if mem_util < 40:
                        recommendations.append(
                            {
                                "metric": "memory",
                                "current_value": mem_util,
                                "recommended_value": mem_util * 0.6,
                                "recommendation": "Consider reducing memory allocation",
                            }
                        )
                    elif mem_util > 85:
                        recommendations.append(
                            {
                                "metric": "memory",
                                "current_value": mem_util,
                                "recommended_value": mem_util * 1.3,
                                "recommendation": "Consider increasing memory allocation",
                            }
                        )

            return recommendations

        except Exception as e:
            self.logger.error(f"Failed to get recommendations: {str(e)}")
            raise

    def get_optimization_metrics(self, resource_id: str) -> Dict[str, Any]:
        """Get optimization metrics for a resource."""
        try:
            metrics = self.predictor.get_historical_metrics(resource_id)
            if metrics.empty:
                return {}

            # Calculate optimization metrics
            return {
                "resource_id": resource_id,
                "metrics": {
                    "utilization": {
                        "cpu": (
                            float(metrics["cpu_utilization"].mean())
                            if "cpu_utilization" in metrics
                            else None
                        ),
                        "memory": (
                            float(metrics["memory_utilization"].mean())
                            if "memory_utilization" in metrics
                            else None
                        ),
                    },
                    "cost": {
                        "current": (
                            float(metrics["cost"].sum()) if "cost" in metrics else None
                        ),
                        "projected": (
                            float(metrics["projected_cost"].sum())
                            if "projected_cost" in metrics
                            else None
                        ),
                    },
                },
            }
        except Exception as e:
            self.logger.error(
                f"Failed to get optimization metrics for {resource_id}: {str(e)}"
            )
            raise
