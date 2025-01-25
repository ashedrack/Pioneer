"""
API routes package
"""
from fastapi import APIRouter
from .resource_management import router as resource_management_router

# Create main API router
router = APIRouter()

# Include sub-routers
router.include_router(resource_management_router, prefix="/resources", tags=["resources"])

__all__ = ['router', 'resource_management_router']
