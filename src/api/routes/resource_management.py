"""
API routes for resource management.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from src.automation.scheduler import ResourceScheduler
from src.ml.models.prediction import MetricsPredictor
from src.api.models import (
    MetricsRequest,
    ScheduleRequest,
    ScheduleResponse,
    MetricsResponse,
    RecommendationsResponse
)

router = APIRouter()

# Dependency injection functions
def get_scheduler() -> ResourceScheduler:
    return ResourceScheduler()

def get_predictor() -> MetricsPredictor:
    return MetricsPredictor()

class ResourceAction(BaseModel):
    resource_id: str
    action: str
    scheduled_time: datetime

class ResourceMetrics(BaseModel):
    resource_id: str
    cpu_usage: float
    memory_usage: float
    network_usage: float
    disk_usage: float
    timestamp: datetime

class ActionResponse(BaseModel):
    status: str
    action: Dict[str, Any]

class ScheduleResponse(BaseModel):
    resource_id: str
    scheduled_actions: Dict[str, Any]

class MetricsResponse(BaseModel):
    status: str
    predictions: Dict[str, Any]

class RecommendationsResponse(BaseModel):
    resource_id: str
    recommendations: List[Dict[str, Any]]

@router.post("/metrics", response_model=MetricsResponse)
async def submit_metrics(
    request: MetricsRequest,
    predictor: MetricsPredictor = Depends(get_predictor)
) -> MetricsResponse:
    """Submit resource metrics"""
    try:
        metrics_data = request.model_dump()
        predictions = predictor.predict(metrics_data)
        return MetricsResponse(
            status="success",
            predictions=predictions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/{resource_id}")
async def get_metrics(
    resource_id: str,
    predictor: MetricsPredictor = Depends(get_predictor)
) -> Dict[str, Any]:
    """Get metrics for a resource"""
    try:
        metrics = predictor.get_historical_metrics(resource_id)
        return {
            "resource_id": resource_id,
            "metrics": metrics.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedule", response_model=ScheduleResponse)
async def schedule_action(
    request: ScheduleRequest,
    scheduler: ResourceScheduler = Depends(get_scheduler)
) -> ScheduleResponse:
    """Schedule a resource action"""
    try:
        schedule_data = request.model_dump()
        scheduler.schedule_action(schedule_data)
        return ScheduleResponse(
            status="scheduled",
            action=schedule_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedule/{resource_id}")
async def get_schedule(
    resource_id: str,
    scheduler: ResourceScheduler = Depends(get_scheduler)
) -> Dict[str, Any]:
    """Get scheduled actions for a resource"""
    try:
        actions = scheduler.get_scheduled_actions(resource_id)
        return {
            "resource_id": resource_id,
            "scheduled_actions": actions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{resource_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    resource_id: str,
    predictor: MetricsPredictor = Depends(get_predictor)
) -> RecommendationsResponse:
    """Get recommendations for a resource"""
    try:
        recommendations = predictor.get_recommendations(resource_id)
        return RecommendationsResponse(
            resource_id=resource_id,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
