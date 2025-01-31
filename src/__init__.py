"""Initialize the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routes
from src.api.routes import router as api_router
from src.auth.routes import router as auth_router

# Create FastAPI app
app = FastAPI(title="Cloud Pioneer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])
