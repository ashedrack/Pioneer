"""Test configuration."""
import os
import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope="session", autouse=True)
def aws_credentials():
    """Mock AWS credentials."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def mock_dynamodb_resource(mocker):
    """Mock DynamoDB resource."""
    mock_resource = MagicMock()
    mock_table = MagicMock()
    mock_resource.Table.return_value = mock_table
    
    # Mock common DynamoDB operations
    mock_table.get_item.return_value = {
        'Item': {
            'resource_id': 'test-instance',
            'timestamp': '2025-01-24T18:10:07Z',
            'metrics': {
                'cpu_utilization': 50.0,
                'memory_utilization': 60.0,
                'network_in': 1000000,
                'network_out': 2000000
            }
        }
    }
    
    mock_table.put_item.return_value = {}
    mock_table.query.return_value = {
        'Items': [{
            'resource_id': 'test-instance',
            'timestamp': '2025-01-24T18:10:07Z',
            'metrics': {
                'cpu_utilization': 50.0,
                'memory_utilization': 60.0,
                'network_in': 1000000,
                'network_out': 2000000
            }
        }]
    }
    
    mocker.patch('boto3.resource', return_value=mock_resource)
    return mock_resource
