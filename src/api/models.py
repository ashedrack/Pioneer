"""API models for request and response validation."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ResourceMetrics(BaseModel):
    """Model for resource metrics data."""

    resource_id: str
    cpu_usage: float
    memory_usage: float
    network_usage: float
    disk_usage: float
    timestamp: datetime


class MetricsRequest(BaseModel):
    """Model for metrics request."""

    resource_id: str
    metrics: List[ResourceMetrics]


class MetricData(BaseModel):
    """Model for metric data."""

    resource_id: str
    timestamp: datetime
    value: float


class MetricsSubmission(BaseModel):
    """Model for metrics submission."""

    resource_id: str
    timestamp: datetime
    metrics: Dict[str, float]


class ResourceOptimizationRequest(BaseModel):
    """Model for resource optimization request."""

    resource_id: str
    days_of_history: int = 30


class ResourceSchedule(BaseModel):
    """Model for resource schedule."""

    resource_id: str
    schedule_type: str  # 'start' or 'stop'
    cron_expression: str
    enabled: bool = True


class ResourceResponse(BaseModel):
    """Model for resource response."""

    id: str
    name: str
    type: str
    region: str
    status: str


class MetricsResponse(BaseModel):
    """Model for metrics response."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    status: str
    predictions: Dict[str, Any]


class OptimizationResponse(BaseModel):
    """Model for optimization response."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_id: str
    recommendations: List[Dict[str, Any]]


class ScheduleResponse(BaseModel):
    """Model for schedule response."""

    resource_id: str
    schedules: List[ResourceSchedule]


class MetricsPrediction(BaseModel):
    """Model for metrics prediction."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_id: str
    predictions: List[Dict[str, Any]]
    confidence: float


class ResourceRecommendation(BaseModel):
    """Model for resource recommendation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_id: str
    recommendation_type: str
    description: str
    estimated_savings: float
    confidence: float


class ScheduledAction(BaseModel):
    """Model for scheduled action."""

    resource_id: str
    action_type: str  # 'start' or 'stop'
    schedule_time: datetime
    recurrence: Optional[str] = None  # cron expression for recurring schedules


class ScheduleRequest(BaseModel):
    """Model for schedule request."""

    resource_id: str
    action_type: str  # 'start' or 'stop'
    schedule_time: datetime
    recurrence: Optional[str] = None  # cron expression for recurring schedules


class RecommendationsResponse(BaseModel):
    """Model for recommendations response."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_id: str
    recommendations: List[Dict[str, Any]]
