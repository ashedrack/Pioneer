import logging
import random
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel
import numpy as np
import statistics
from fastapi import APIRouter, HTTPException, Request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Store utilization history
utilization_history = []
MAX_HISTORY_POINTS = 50

def generate_dummy_metrics():
    return {
        "cpu_usage": random.uniform(20, 95),
        "memory_usage": random.uniform(30, 90),
        "disk_usage": random.uniform(40, 85),
        "cost_savings": random.uniform(10000, 20000),
        "error_rate": random.uniform(0, 50),
        "latency": random.uniform(1, 5),
    }

def generate_utilization_data(days: int = 7) -> List[Dict]:
    data = []
    base_date = datetime.now()
    for i in range(days * 24):  # Hourly data
        timestamp = base_date - timedelta(hours=i)
        data.append(
            {"timestamp": timestamp.isoformat(), "value": random.uniform(60, 95)}
        )
    return data

def generate_cost_data(months: int = 6) -> List[Dict]:
    data = []
    base_date = datetime.now()
    for i in range(months):
        month = (base_date - timedelta(days=30 * i)).strftime("%b")
        actual = random.uniform(10000, 15000)
        data.append(
            {
                "month": month,
                "actual": actual,
                "predicted": actual * random.uniform(1.1, 1.3),
            }
        )
    return data[::-1]  # Reverse to get chronological order

def get_cpu_utilization():
    return {
        "timestamp": datetime.now().isoformat(),
        "value": psutil.cpu_percent(interval=1)
    }

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

def generate_cost_prediction(actual_costs: List[float], num_future_months: int = 3) -> List[float]:
    """Generate cost predictions using simple linear regression."""
    x = np.arange(len(actual_costs))
    y = np.array(actual_costs)
    
    # Fit linear regression
    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients
    
    # Generate future predictions
    future_x = np.arange(len(actual_costs), len(actual_costs) + num_future_months)
    predictions = slope * future_x + intercept
    
    return predictions.tolist()

@router.get("/overall")
async def get_overall_metrics(request: Request):
    logger.info(f"Received request for overall metrics. URL: {request.url}")
    try:
        logger.info("Fetching overall metrics")
        metrics = generate_dummy_metrics()
        logger.info(f"Overall metrics generated: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error generating overall metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating overall metrics")

@router.get("/utilization/trend")
async def get_utilization_trend(request: Request):
    logger.info(f"Received request for utilization trend. URL: {request.url}")
    try:
        logger.info("Fetching utilization trend data")
        data = generate_utilization_data()
        logger.info(f"Generated {len(data)} utilization data points")
        return data
    except Exception as e:
        logger.error(f"Error generating utilization trend data: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error generating utilization trend data"
        )

@router.get("/utilization/current")
async def get_current_utilization():
    """Get current CPU utilization."""
    try:
        data = get_cpu_utilization()
        utilization_history.append(data)
        
        # Keep only last MAX_HISTORY_POINTS
        if len(utilization_history) > MAX_HISTORY_POINTS:
            utilization_history.pop(0)
        
        return data
    except Exception as e:
        logger.error(f"Error getting current utilization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/utilization/history")
async def get_utilization_history():
    """Get CPU utilization history."""
    try:
        return utilization_history
    except Exception as e:
        logger.error(f"Error getting utilization history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cost/analysis")
async def get_cost_analysis(request: Request):
    logger.info(f"Received request for cost analysis. URL: {request.url}")
    try:
        logger.info("Fetching cost analysis data")
        data = generate_cost_data()
        logger.info(f"Generated {len(data)} cost data points")
        return data
    except Exception as e:
        logger.error(f"Error generating cost analysis data: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error generating cost analysis data"
        )

@router.post("/cost/analysis")
async def get_cost_analysis_with_date_range(date_range: DateRange):
    """Get cost analysis data with predictions."""
    try:
        # Calculate number of months in the date range
        months_diff = (date_range.end_date.year - date_range.start_date.year) * 12 + \
                     date_range.end_date.month - date_range.start_date.month
        
        # Generate base cost with some randomization and trend
        base_cost = 10000  # Base monthly cost
        monthly_increase = 500  # Average monthly increase
        variation = 0.1  # 10% random variation
        
        actual_costs = []
        current_date = date_range.start_date
        
        # Generate actual costs for past months
        while current_date <= datetime.now():
            if current_date > date_range.end_date:
                break
                
            month_number = (current_date.year - date_range.start_date.year) * 12 + \
                          (current_date.month - date_range.start_date.month)
            
            # Calculate cost with trend and randomization
            cost = base_cost + (monthly_increase * month_number)
            random_factor = 1 + random.uniform(-variation, variation)
            actual_cost = cost * random_factor
            
            actual_costs.append(round(actual_cost, 2))
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        # Generate predictions for future months
        predictions = generate_cost_prediction(actual_costs)
        
        # Prepare response data
        cost_data = []
        current_date = date_range.start_date
        
        for i, cost in enumerate(actual_costs):
            month_str = current_date.strftime("%Y-%m")
            cost_data.append({
                "month": month_str,
                "actual": cost,
                "predicted": None
            })
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        # Add future predictions
        for i, predicted_cost in enumerate(predictions):
            if current_date > date_range.end_date:
                break
            month_str = current_date.strftime("%Y-%m")
            cost_data.append({
                "month": month_str,
                "actual": None,
                "predicted": round(predicted_cost, 2)
            })
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        return {
            "data": cost_data,
            "summary": {
                "total_actual": sum(c["actual"] for c in cost_data if c["actual"] is not None),
                "average_monthly": statistics.mean(c["actual"] for c in cost_data if c["actual"] is not None),
                "predicted_next_month": predictions[0] if predictions else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating cost analysis data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating cost analysis data: {str(e)}"
        )

@router.get("/status")
async def get_resource_status():
    """Get current resource status counts and system metrics."""
    try:
        cpu_usage = psutil.cpu_percent()
        memory_usage = get_memory_usage()
        
        # Simulate resource counts based on system metrics
        total_resources = 50 + random.randint(-5, 5)
        warning_threshold = 70
        error_threshold = 90
        
        # Calculate resource counts based on current system metrics
        if cpu_usage > error_threshold or memory_usage > error_threshold:
            healthy = total_resources - random.randint(15, 20)
            warning = random.randint(10, 15)
            no_data = total_resources - healthy - warning
        elif cpu_usage > warning_threshold or memory_usage > warning_threshold:
            healthy = total_resources - random.randint(8, 12)
            warning = random.randint(5, 8)
            no_data = total_resources - healthy - warning
        else:
            healthy = total_resources - random.randint(3, 5)
            warning = random.randint(2, 4)
            no_data = total_resources - healthy - warning
        
        return {
            "healthy": healthy,
            "warning": warning,
            "noData": no_data,
            "metrics": {
                "cpuUsage": cpu_usage,
                "memoryUsage": memory_usage
            }
        }
    except Exception as e:
        logger.error(f"Error getting resource status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resource/status")
async def get_resource_status_legacy(request: Request):
    logger.info(f"Received request for resource status. URL: {request.url}")
    try:
        logger.info("Fetching resource status")
        status = {
            "warning": random.randint(0, 3),
            "ok": random.randint(45, 60),
            "error": random.randint(0, 2),
        }
        logger.info(f"Resource status generated: {status}")
        return status
    except Exception as e:
        logger.error(f"Error generating resource status: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error generating resource status"
        )

@router.get("/{resource_id}")
async def get_resource_metrics(request: Request, resource_id: str):
    logger.info(f"Received request for resource metrics. URL: {request.url}")
    try:
        logger.info(f"Fetching metrics for resource {resource_id}")
        metrics = {
            "resource_id": resource_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": generate_dummy_metrics(),
        }
        logger.info(f"Generated metrics for resource {resource_id}: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error generating metrics for resource {resource_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating metrics for resource {resource_id}",
        )
