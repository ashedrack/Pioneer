from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import random
from typing import List, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

def generate_dummy_metrics():
    return {
        "cpu_usage": random.uniform(20, 95),
        "memory_usage": random.uniform(30, 90),
        "disk_usage": random.uniform(40, 85),
        "cost_savings": random.uniform(10000, 20000),
        "error_rate": random.uniform(0, 50),
        "latency": random.uniform(1, 5)
    }

def generate_utilization_data(days: int = 7) -> List[Dict]:
    data = []
    base_date = datetime.now()
    for i in range(days * 24):  # Hourly data
        timestamp = base_date - timedelta(hours=i)
        data.append({
            "timestamp": timestamp.isoformat(),
            "value": random.uniform(60, 95)
        })
    return data

def generate_cost_data(months: int = 6) -> List[Dict]:
    data = []
    base_date = datetime.now()
    for i in range(months):
        month = (base_date - timedelta(days=30 * i)).strftime("%b")
        actual = random.uniform(10000, 15000)
        data.append({
            "month": month,
            "actual": actual,
            "predicted": actual * random.uniform(1.1, 1.3)
        })
    return data[::-1]  # Reverse to get chronological order

@router.get("/overall")
async def get_overall_metrics():
    try:
        logger.info("Fetching overall metrics")
        metrics = generate_dummy_metrics()
        logger.info(f"Overall metrics generated: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error generating overall metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating overall metrics")

@router.get("/utilization/trend")
async def get_utilization_trend():
    try:
        logger.info("Fetching utilization trend data")
        data = generate_utilization_data()
        logger.info(f"Generated {len(data)} utilization data points")
        return data
    except Exception as e:
        logger.error(f"Error generating utilization trend data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating utilization trend data")

@router.get("/cost/analysis")
async def get_cost_analysis():
    try:
        logger.info("Fetching cost analysis data")
        data = generate_cost_data()
        logger.info(f"Generated {len(data)} cost data points")
        return data
    except Exception as e:
        logger.error(f"Error generating cost analysis data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating cost analysis data")

@router.get("/resource/status")
async def get_resource_status():
    try:
        logger.info("Fetching resource status")
        status = {
            "warning": random.randint(0, 3),
            "ok": random.randint(45, 60),
            "no_data": random.randint(0, 2)
        }
        logger.info(f"Resource status generated: {status}")
        return status
    except Exception as e:
        logger.error(f"Error generating resource status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating resource status")

@router.get("/{resource_id}")
async def get_resource_metrics(resource_id: str):
    try:
        logger.info(f"Fetching metrics for resource {resource_id}")
        metrics = {
            "resource_id": resource_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": generate_dummy_metrics()
        }
        logger.info(f"Generated metrics for resource {resource_id}: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error generating metrics for resource {resource_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating metrics for resource {resource_id}")
