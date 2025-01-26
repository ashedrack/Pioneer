"""Test configuration and fixtures for Cloud Pioneer.

This module contains shared fixtures and configuration for all test modules.
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Add project root to Python path if not already added
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.main import app  # noqa: E402

# Configure test environment
os.environ.setdefault("ENVIRONMENT", "test")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables before each test."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test-key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test-secret"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    yield
    # Clean up environment after test
    for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]:
        os.environ.pop(key, None)

@pytest.fixture
def mock_dynamodb_resource(mocker):
    """Mock DynamoDB resource."""
    mock_resource = MagicMock()
    mock_table = MagicMock()
    mock_resource.Table.return_value = mock_table

    # Mock common DynamoDB operations
    mock_table.get_item.return_value = {
        "Item": {
            "resource_id": "test-instance",
            "timestamp": "2025-01-24T18:10:07Z",
            "metrics": {
                "cpu_utilization": 50.0,
                "memory_utilization": 60.0,
                "network_in": 1000000,
                "network_out": 2000000,
            },
        }
    }

    mock_table.put_item.return_value = {}
    mock_table.query.return_value = {
        "Items": [
            {
                "resource_id": "test-instance",
                "timestamp": "2025-01-24T18:10:07Z",
                "metrics": {
                    "cpu_utilization": 50.0,
                    "memory_utilization": 60.0,
                    "network_in": 1000000,
                    "network_out": 2000000,
                },
            }
        ]
    }

    mocker.patch("boto3.resource", return_value=mock_resource)
    return mock_resource
