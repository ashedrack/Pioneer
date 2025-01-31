"""Cost optimization routes."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import APIRouter, HTTPException
import random

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cost-optimization", tags=["cost-optimization"])

COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

def generate_cost_distribution():
    """Generate mock cost distribution data."""
    categories = [
        {"name": "Compute", "base": 5200},
        {"name": "Storage", "base": 3800},
        {"name": "Network", "base": 2500},
        {"name": "Database", "base": 1800},
        {"name": "Other", "base": 1200}
    ]
    
    distribution = []
    for i, cat in enumerate(categories):
        # Add some randomness to the base values
        value = cat["base"] + random.randint(-200, 200)
        distribution.append({
            "category": cat["name"],
            "value": value,
            "color": COLORS[i % len(COLORS)]
        })
    
    return distribution

def generate_forecast_data():
    """Generate mock forecast data."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    base_cost = 15000
    monthly_increase = 500
    optimization_savings = 2000
    
    forecast_data = []
    for i, month in enumerate(months):
        actual = None if i >= 3 else base_cost + (monthly_increase * i) + random.randint(-200, 200)
        forecast = base_cost + (monthly_increase * i) if i >= 3 else None
        optimized = (base_cost + (monthly_increase * i) - optimization_savings) if i >= 3 else None
        
        forecast_data.append({
            "month": month,
            "actual": actual,
            "forecast": forecast,
            "optimized": optimized
        })
    
    return forecast_data

def generate_recommendations():
    """Generate mock cost optimization recommendations."""
    recommendations = [
        {
            "id": "REC001",
            "title": "Optimize Instance Types",
            "description": "Several instances are consistently underutilized. Rightsizing these instances could reduce costs while maintaining performance.",
            "impact": "High",
            "savings": 1200,
            "effort": "Medium",
            "category": "Compute",
            "resources": [
                "prod-app-server-1",
                "prod-app-server-2",
                "staging-db-1"
            ]
        },
        {
            "id": "REC002",
            "title": "Remove Unused Storage Volumes",
            "description": "Multiple unattached storage volumes have been identified. Removing these unused resources will reduce storage costs.",
            "impact": "Medium",
            "savings": 800,
            "effort": "Low",
            "category": "Storage",
            "resources": [
                "vol-0a1b2c3d4e5f",
                "vol-1b2c3d4e5f6g",
                "vol-2c3d4e5f6g7h"
            ]
        },
        {
            "id": "REC003",
            "title": "Implement Auto-Scaling",
            "description": "Implementing auto-scaling for your application servers could reduce costs during low-traffic periods while maintaining performance during peak times.",
            "impact": "High",
            "savings": 2000,
            "effort": "High",
            "category": "Compute",
            "resources": [
                "prod-web-cluster",
                "prod-app-cluster"
            ]
        }
    ]
    return recommendations

@router.get("/distribution")
async def get_cost_distribution():
    """Get cost distribution by category."""
    try:
        distribution = generate_cost_distribution()
        return {
            "data": distribution,
            "total": sum(item["value"] for item in distribution)
        }
    except Exception as e:
        logger.error(f"Error getting cost distribution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast")
async def get_cost_forecast():
    """Get cost forecast data."""
    try:
        forecast_data = generate_forecast_data()
        current_month = next((d for d in forecast_data if d["forecast"] is not None), None)
        
        return {
            "data": forecast_data,
            "summary": {
                "currentMonth": current_month["forecast"] if current_month else 0,
                "potentialSavings": (current_month["forecast"] - current_month["optimized"]) if current_month else 0
            }
        }
    except Exception as e:
        logger.error(f"Error getting cost forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_recommendations():
    """Get cost optimization recommendations."""
    try:
        recommendations = generate_recommendations()
        total_savings = sum(rec["savings"] for rec in recommendations)
        
        return {
            "recommendations": recommendations,
            "summary": {
                "totalRecommendations": len(recommendations),
                "potentialSavings": total_savings
            }
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{recommendation_id}")
async def get_recommendation_details(recommendation_id: str):
    """Get detailed information about a specific recommendation."""
    try:
        recommendations = generate_recommendations()
        recommendation = next((r for r in recommendations if r["id"] == recommendation_id), None)
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        
        # Add additional details for the detailed view
        recommendation["details"] = {
            "implementation_steps": [
                "1. Review current resource utilization patterns",
                "2. Create backup of current configuration",
                "3. Schedule maintenance window",
                "4. Apply recommended changes",
                "5. Monitor performance for 24-48 hours",
                "6. Document changes and update runbooks"
            ],
            "risks": [
                "Temporary service interruption during implementation",
                "Potential performance impact during adjustment period",
                "Dependencies may need reconfiguration"
            ],
            "prerequisites": [
                "Full backup of affected resources",
                "Approved maintenance window",
                "Required access permissions",
                "Updated monitoring alerts"
            ]
        }
        
        return recommendation
    except Exception as e:
        logger.error(f"Error getting recommendation details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
