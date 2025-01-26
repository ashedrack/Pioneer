import os
from typing import List

from pydantic_settings import BaseSettings


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
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/resource_predictor.h5")
    TRAINING_BATCH_SIZE: int = 32
    TRAINING_EPOCHS: int = 100

    # Resource Management
    SHUTDOWN_NOTICE_PERIOD: int = 30  # minutes
    MIN_IDLE_PERIOD: int = 60  # minutes
    MAX_RESOURCE_WAIT: int = 300  # seconds
    OPTIMIZATION_INTERVAL: int = 15  # minutes

    # Cloud Provider Settings
    SUPPORTED_CLOUDS: List[str] = ["aws", "gcp", "azure"]

    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    KAFKA_CLIENT_ID: str = os.getenv("KAFKA_CLIENT_ID", "cloud-pioneer")
    KAFKA_METRICS_TOPIC: str = "cloud-pioneer-metrics"
    KAFKA_EVENTS_TOPIC: str = "cloud-pioneer-events"

    # Metrics Collection
    METRICS_COLLECTION_INTERVAL: int = 60  # seconds
    METRICS_BATCH_SIZE: int = 100
    METRICS_RETENTION_DAYS: int = 30

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Redis Cache
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    class Config:
        case_sensitive = True


settings = Settings()
