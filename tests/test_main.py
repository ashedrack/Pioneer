"""Test main API endpoints."""
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.main import app, get_predictor, get_scheduler, get_optimizer
from src.ml.models.prediction import MetricsPredictor
from src.automation.scheduler import ResourceScheduler
from src.automation.optimizer import ResourceOptimizer

@pytest.fixture
def test_metrics():
    """Test metrics data."""
    return {
        'resource_id': 'test-instance',
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'cpu_utilization': 50.0,
            'memory_utilization': 60.0,
            'network_in': 1000000,
            'network_out': 2000000
        }
    }

@pytest.fixture
def test_schedule():
    """Test schedule data."""
    return {
        'resource_id': 'test-instance',
        'action': 'stop',
        'scheduled_time': (datetime.now() + timedelta(hours=1)).isoformat()
    }

@pytest.fixture
async def predictor(mock_dynamodb_resource):
    """Create predictor instance."""
    return MetricsPredictor(dynamodb=mock_dynamodb_resource)

@pytest.fixture
async def scheduler(mock_dynamodb_resource):
    """Create scheduler instance."""
    return ResourceScheduler(dynamodb=mock_dynamodb_resource)

@pytest.fixture
async def optimizer(predictor):
    """Create optimizer instance."""
    return ResourceOptimizer(predictor=predictor)

@pytest.fixture
async def test_client(predictor, scheduler, optimizer):
    """Test client fixture with dependencies."""
    app.dependency_overrides[get_predictor] = lambda: predictor
    app.dependency_overrides[get_scheduler] = lambda: scheduler
    app.dependency_overrides[get_optimizer] = lambda: optimizer
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_metrics(test_client):
    """Test get metrics endpoint."""
    response = test_client.get("/metrics/test-instance")
    assert response.status_code == 200
    data = response.json()
    assert data['resource_id'] == 'test-instance'
    assert 'metrics' in data

@pytest.mark.asyncio
async def test_get_metrics_not_found(test_client, mock_dynamodb_resource):
    """Test get metrics endpoint with non-existent resource."""
    mock_dynamodb_resource.Table().get_item.side_effect = HTTPException(status_code=404, detail="Resource not found")
    response = test_client.get("/metrics/non-existent")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_post_metrics(test_client, test_metrics):
    """Test post metrics endpoint."""
    response = test_client.post("/metrics", json=test_metrics)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_schedule(test_client):
    """Test get schedule endpoint."""
    response = test_client.get("/schedule/test-instance")
    assert response.status_code == 200
    data = response.json()
    assert data['resource_id'] == 'test-instance'

@pytest.mark.asyncio
async def test_get_schedule_not_found(test_client, mock_dynamodb_resource):
    """Test get schedule endpoint with non-existent resource."""
    mock_dynamodb_resource.Table().get_item.side_effect = HTTPException(status_code=404, detail="Resource not found")
    response = test_client.get("/schedule/non-existent")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_post_schedule(test_client, test_schedule):
    """Test post schedule endpoint."""
    response = test_client.post("/schedule", json=test_schedule)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_optimize_resources(test_client):
    """Test optimize resources endpoint."""
    response = test_client.post("/optimize", json={"resource_ids": ["test-instance"]})
    assert response.status_code == 200
