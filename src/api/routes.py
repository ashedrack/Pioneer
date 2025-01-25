from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from ..ml.resource_optimizer import ResourceOptimizer
from ..automation.scheduler import ResourceScheduler, AutomationTask
from pydantic import BaseModel
import random

router = APIRouter()
security = HTTPBearer()

class MetricData(BaseModel):
    resource_id: str
    metric_name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]

class ScheduleRequest(BaseModel):
    resource_id: str
    action: str
    schedule_time: datetime
    parameters: Dict[str, Any]

class OptimizationRequest(BaseModel):
    resource_id: str
    days_of_history: int = 30

# In-memory storage for metrics (replace with database in production)
metrics_db: Dict[str, List[dict]] = {}

def generate_dummy_metrics(resource_id: str, days: int = 7) -> List[dict]:
    """Generate dummy metrics data for the past N days"""
    metrics = []
    now = datetime.utcnow()
    
    for i in range(days * 24):  # 24 data points per day
        timestamp = now - timedelta(hours=i)
        metrics.append({
            "resource_id": resource_id,
            "timestamp": timestamp.isoformat() + "Z",
            "metrics": {
                "cpu_usage": round(random.uniform(20, 80), 2),
                "memory_usage": round(random.uniform(30, 90), 2),
                "disk_usage": round(random.uniform(40, 95), 2),
                "network_in": round(random.uniform(100, 1000), 2),
                "network_out": round(random.uniform(100, 1000), 2)
            }
        })
    
    return sorted(metrics, key=lambda x: x["timestamp"])

@router.post("/metrics")
async def submit_metrics(
    metrics: List[MetricData],
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Submit metrics for processing."""
    try:
        # Process metrics (implement your logic here)
        return {"status": "success", "message": f"Processed {len(metrics)} metrics"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedule")
async def schedule_task(
    request: ScheduleRequest,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Schedule a resource management task."""
    try:
        task = AutomationTask(
            resource_id=request.resource_id,
            action=request.action,
            schedule_time=request.schedule_time,
            parameters=request.parameters
        )
        
        scheduler = ResourceScheduler({})  # Add your config here
        success = scheduler.schedule_task(task)
        
        if success:
            return {"status": "success", "message": "Task scheduled successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to schedule task")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedule/{resource_id}")
async def get_schedule(
    resource_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Get scheduled tasks for a resource."""
    try:
        scheduler = ResourceScheduler({})  # Add your config here
        tasks = scheduler.get_task_status(resource_id)
        return {"status": "success", "tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize")
async def optimize_resource(
    request: OptimizationRequest,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Generate optimized schedule for a resource."""
    try:
        # Get historical data (implement your data retrieval logic)
        historical_data = pd.DataFrame()  # Replace with actual data
        
        optimizer = ResourceOptimizer({})  # Add your config here
        predictions = optimizer.predict_utilization(historical_data)
        
        scheduler = ResourceScheduler({})  # Add your config here
        recommendations = scheduler.optimize_schedule(request.resource_id, historical_data)
        
        return {
            "status": "success",
            "predictions": predictions,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}

@router.post("/metrics/dummy")
async def submit_dummy_metrics(
    metrics: List[MetricData],
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if metrics[0].resource_id not in metrics_db:
        metrics_db[metrics[0].resource_id] = []
    
    metrics_db[metrics[0].resource_id].append({"resource_id": metrics[0].resource_id, "timestamp": metrics[0].timestamp.isoformat() + "Z", "metrics": {"cpu_usage": metrics[0].value}})
    return {"status": "success", "message": "Metrics stored successfully"}

@router.get("/metrics/{resource_id}/dummy")
async def get_dummy_metrics(
    resource_id: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # If no metrics exist, generate dummy data
    if resource_id not in metrics_db or not metrics_db[resource_id]:
        metrics_db[resource_id] = generate_dummy_metrics(resource_id)
    
    return {
        "status": "success",
        "data": {
            "resource_id": resource_id,
            "metrics": metrics_db[resource_id]
        }
    }

@router.get("/resources")
async def get_resources(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Get list of resources with dummy data"""
    resources = [
        {
            "id": "server-001",
            "name": "Production Web Server",
            "type": "t2.medium",
            "region": "us-west",
            "status": "running"
        },
        {
            "id": "server-002",
            "name": "Database Server",
            "type": "t2.large",
            "region": "us-west",
            "status": "running"
        },
        {
            "id": "server-003",
            "name": "Test Environment",
            "type": "t2.small",
            "region": "us-east",
            "status": "stopped"
        }
    ]
    
    # Generate metrics for each resource if they don't exist
    for resource in resources:
        if resource["id"] not in metrics_db:
            metrics_db[resource["id"]] = generate_dummy_metrics(resource["id"])
    
    return {
        "status": "success",
        "data": resources
    }
