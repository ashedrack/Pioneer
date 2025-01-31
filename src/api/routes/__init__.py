"""
API routes package
"""

from fastapi import APIRouter

from .resource_management import router as resource_management_router
from .metrics import router as metrics_router
from .cost_optimization import router as cost_optimization_router
from .process_management import router as process_management_router
from .auth import router as auth_router

# Create main API router
router = APIRouter()

# Include sub-routers
router.include_router(auth_router)
router.include_router(
    resource_management_router, prefix="/resources", tags=["resources"]
)
router.include_router(
    cost_optimization_router, prefix="/cost-optimization", tags=["cost-optimization"]
)
router.include_router(
    process_management_router, prefix="/processes", tags=["processes"]
)

__all__ = [
    "router",
    "resource_management_router",
    "metrics_router",
    "cost_optimization_router",
    "process_management_router",
    "auth_router"
]
