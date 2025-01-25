"""Main FastAPI application."""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
import uvicorn

from src.ml.predictor import ResourcePredictor
from src.automation.scheduler import ResourceScheduler
from src.automation.optimizer import ResourceOptimizer
from src.api.models import (
    MetricsSubmission,
    MetricsPrediction,
    ResourceRecommendation,
    ScheduledAction,
    ScheduleResponse
)
from src.auth.routes import router as auth_router
from src.api.routes import router as api_router
from src.api.routes import metrics

app = FastAPI(title="Cloud Pioneer")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton instances
_predictor = None
_scheduler = None
_optimizer = None

def get_predictor() -> ResourcePredictor:
    """Get metrics predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = ResourcePredictor()
    return _predictor

def get_scheduler() -> ResourceScheduler:
    """Get resource scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = ResourceScheduler()
    return _scheduler

def get_optimizer() -> ResourceOptimizer:
    """Get resource optimizer instance."""
    global _optimizer
    if _optimizer is None:
        _optimizer = ResourceOptimizer()
    return _optimizer

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Cloud Pioneer"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/v1/metrics")
async def submit_metrics(
    metrics: MetricsSubmission,
    predictor: ResourcePredictor = Depends(get_predictor)
) -> Dict[str, Any]:
    """Submit resource metrics."""
    try:
        data = metrics.model_dump()
        predictor.store_metrics(
            resource_id=data['resource_id'],
            timestamp=data['timestamp'],
            metrics=data['metrics']
        )
        return {"status": "success", "message": "Metrics stored successfully"}
    except Exception as e:
        logger.error(f"Error submitting metrics: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/metrics/{resource_id}")
async def get_metrics(
    resource_id: str,
    predictor: ResourcePredictor = Depends(get_predictor)
) -> Dict[str, Any]:
    """Get resource metrics."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        metrics = predictor.get_historical_metrics(
            resource_id=resource_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )
        return {
            "status": "success",
            "data": {
                "resource_id": resource_id,
                "metrics": metrics
            }
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/recommendations/{resource_id}")
async def get_recommendations(
    resource_id: str,
    optimizer: ResourceOptimizer = Depends(get_optimizer)
) -> Dict[str, Any]:
    """Get resource optimization recommendations."""
    try:
        recommendations = optimizer.get_recommendations(resource_id)
        return {"status": "success", "data": recommendations}
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/v1/schedule")
async def schedule_action(
    action: ScheduledAction,
    scheduler: ResourceScheduler = Depends(get_scheduler)
) -> Dict[str, Any]:
    """Schedule a resource action."""
    try:
        data = action.model_dump()
        result = scheduler.schedule_action(
            resource_id=data['resource_id'],
            action=data['action'],
            scheduled_time=data['scheduled_time']
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error scheduling action: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/schedule/{resource_id}")
async def get_schedule(
    resource_id: str,
    scheduler: ResourceScheduler = Depends(get_scheduler)
) -> Dict[str, Any]:
    """Get scheduled actions for a resource."""
    try:
        actions = scheduler.get_scheduled_actions(resource_id)
        return {"status": "success", "data": actions}
    except Exception as e:
        logger.error(f"Error getting schedule: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
