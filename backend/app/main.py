from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

app = FastAPI(title="Pioneer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UtilizationData(BaseModel):
    timestamp: str
    value: float

class ResourceStatus(BaseModel):
    warning: int
    ok: int
    no_data: int

class CostData(BaseModel):
    month: str
    actual: float
    predicted: float

@app.get("/api/metrics/status", response_model=ResourceStatus)
async def get_metrics_status():
    """Get the current status metrics of resources"""
    return {
        "ok": 42,
        "warning": 7,
        "no_data": 2
    }

@app.get("/api/metrics/utilization", response_model=List[UtilizationData])
async def get_metrics_utilization():
    """Get utilization metrics over time"""
    now = datetime.utcnow()
    data = []
    for i in range(24):  # Last 24 hours
        timestamp = (now - timedelta(hours=i)).isoformat()
        data.append({
            "timestamp": timestamp,
            "value": random.uniform(20, 80)
        })
    return data

@app.get("/api/metrics/cost", response_model=List[CostData])
async def get_metrics_cost():
    """Get cost metrics including actual and predicted costs per month"""
    now = datetime.utcnow()
    data = []
    for i in range(6):  # Last 6 months
        month = (now - timedelta(days=30 * i)).strftime("%Y-%m")
        data.append({
            "month": month,
            "actual": random.uniform(10000, 15000),
            "predicted": random.uniform(12000, 18000)
        })
    return data

class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    impact: float

class CostBreakdown(BaseModel):
    compute: float
    storage: float
    network: float

class CostOptimizationResponse(BaseModel):
    costs: CostBreakdown
    total_cost: float
    potential_savings: float
    savings_percentage: float
    recommendations: List[Recommendation]

@app.get("/api/v1/costs/optimization", response_model=CostOptimizationResponse)
async def get_cost_optimization():
    """
    Get cost optimization data including current costs, potential savings,
    and recommendations for cost reduction.
    """
    try:
        return {
            "costs": {
                "compute": 1200.00,
                "storage": 800.00,
                "network": 400.00
            },
            "total_cost": 2400.00,
            "potential_savings": 600.00,
            "savings_percentage": 25.0,
            "recommendations": [
                {
                    "id": "1",
                    "title": "Optimize compute resources",
                    "description": "Consider right-sizing underutilized instances based on CPU and memory usage patterns",
                    "impact": 300.00
                },
                {
                    "id": "2",
                    "title": "Storage optimization",
                    "description": "Move infrequently accessed data to lower-cost storage tiers",
                    "impact": 200.00
                },
                {
                    "id": "3",
                    "title": "Network cost reduction",
                    "description": "Optimize data transfer patterns and use caching where possible",
                    "impact": 100.00
                }
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve cost optimization data: {str(e)}"
        )

# Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to Cloud Pioneer"}
