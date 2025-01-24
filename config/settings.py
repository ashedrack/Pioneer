from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CloudPioneer"
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "cloudpioneer")
    
    # ML Model Settings
    MODEL_UPDATE_INTERVAL: int = 24  # hours
    PREDICTION_WINDOW: int = 168  # hours (1 week)
    
    # Resource Management
    SHUTDOWN_NOTICE_PERIOD: int = 30  # minutes
    MIN_IDLE_PERIOD: int = 60  # minutes
    
    # Cloud Provider Settings
    SUPPORTED_CLOUDS: List[str] = ["aws", "gcp", "azure"]
    
    class Config:
        case_sensitive = True

settings = Settings()
