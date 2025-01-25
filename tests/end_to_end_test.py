"""End-to-end tests for Cloud Pioneer"""
import unittest
import requests
import json
import time
import boto3
import os
import subprocess
import psutil
import docker
from datetime import datetime, timedelta
import pandas as pd
from src.api.key_management import APIKeyManager
from src.ml.resource_optimizer import ResourceOptimizer
from src.automation.scheduler import ResourceScheduler
import pytest
from moto import mock_dynamodb, mock_s3, mock_ec2
from fastapi.testclient import TestClient
from src.main import app
from src.agent.agent import MonitoringAgent
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="class")
def aws_setup():
    """Set up AWS mocks and credentials"""
    with mock_dynamodb(), mock_s3(), mock_ec2():
        # Set up AWS credentials
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

        # Create DynamoDB tables
        dynamodb = boto3.resource('dynamodb')
        
        # Create metrics table
        dynamodb.create_table(
            TableName='cloud_pioneer_metrics',
            KeySchema=[
                {'AttributeName': 'resource_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'resource_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Create schedules table
        dynamodb.create_table(
            TableName='cloud_pioneer_schedules',
            KeySchema=[
                {'AttributeName': 'resource_id', 'KeyType': 'HASH'},
                {'AttributeName': 'scheduled_time', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'resource_id', 'AttributeType': 'S'},
                {'AttributeName': 'scheduled_time', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Create S3 bucket
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket='cloud-pioneer-models')

        yield {
            'dynamodb': dynamodb,
            's3': boto3.client('s3'),
            'ec2': boto3.client('ec2')
        }

@pytest.mark.usefixtures("aws_setup")
class CloudPioneerE2ETest(unittest.IsolatedAsyncioTestCase):
    """End-to-end test suite for Cloud Pioneer"""

    @pytest.fixture(autouse=True)
    def setup_test_environment(self, aws_setup, tmp_path):
        """Set up test environment"""
        self.aws = aws_setup
        self.test_dir = tmp_path

        # Create test config
        config = {
            'agent': {
                'collection_interval': 60,
                'shipping_interval': 10
            },
            'backends': {
                'aws': {
                    'enabled': True,
                    'region': 'us-east-1'
                }
            },
            'collectors': {
                'system': {
                    'enabled': True
                }
            }
        }

        # Write config file
        config_path = self.test_dir / 'config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f)

        self.config_path = str(config_path)
        
        # Create key manager
        self.key_manager = MagicMock()
        self.key_manager.get_key.return_value = 'test-key'

    async def setUp(self):
        """Set up test environment"""
        # Set AWS credentials and region for testing
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        
        # Initialize AWS clients with endpoint_url for localstack
        self.dynamodb = boto3.client('dynamodb',
                                   region_name='us-east-1',
                                   endpoint_url='http://localhost:4566',
                                   aws_access_key_id='testing',
                                   aws_secret_access_key='testing')
        
        self.s3 = boto3.client('s3',  # Don't specify region for S3 client
                              endpoint_url='http://localhost:4566',
                              aws_access_key_id='testing',
                              aws_secret_access_key='testing')
        
        self.ec2 = boto3.client('ec2',
                               region_name='us-east-1',
                               endpoint_url='http://localhost:4566',
                               aws_access_key_id='testing',
                               aws_secret_access_key='testing')

        # Create test resources
        await self._create_test_resources()
        
    async def tearDown(self):
        # Cleanup test resources
        await self._cleanup_test_resources()

    async def _create_test_resources(self):
        """Create necessary AWS resources for testing"""
        try:
            # Create DynamoDB table
            self.dynamodb.create_table(
                TableName='cloud_pioneer_metrics',
                KeySchema=[
                    {'AttributeName': 'resource_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'resource_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Create S3 bucket
            self.s3.create_bucket(Bucket='cloud-pioneer-test-bucket')
        except self.dynamodb.exceptions.ResourceInUseException:
            # Table already exists
            pass
        except self.s3.exceptions.BucketAlreadyExists:
            # Bucket already exists
            pass

    async def _cleanup_test_resources(self):
        """Clean up AWS resources after testing"""
        try:
            # Delete DynamoDB table
            self.dynamodb.delete_table(TableName='cloud_pioneer_metrics')
            
            # Delete S3 bucket
            self.s3.delete_bucket(Bucket='cloud-pioneer-test-bucket')
        except:
            pass

    async def test_01_agent_installation(self):
        """Test agent installation process"""
        print("\nTesting agent installation...")
        
        # Download installation script
        response = requests.get(
            'https://storage.googleapis.com/cloud-pioneer-agent/install.sh'
        )
        self.assertEqual(response.status_code, 200)
        
        # Save and execute installation script
        with open('install.sh', 'wb') as f:
            f.write(response.content)
        
        # Make script executable and run it
        os.chmod('install.sh', 0o755)
        result = subprocess.run(
            ['./install.sh', '-k', self.api_key],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        
        # Verify agent service is running
        time.sleep(5)  # Wait for service to start
        agent_running = False
        for proc in psutil.process_iter(['name']):
            if 'cloudpioneer-agent' in proc.info['name']:
                agent_running = True
                break
        self.assertTrue(agent_running)
        
        print("✓ Agent installation test passed")
    
    async def test_02_metric_collection(self):
        """Test metric collection functionality"""
        print("\nTesting metric collection...")
        
        # Create a test container to monitor
        container = self.docker_client.containers.run(
            "nginx:latest",
            name="test-nginx",
            detach=True
        )
        
        # Wait for metrics to be collected
        time.sleep(30)
        
        # Query metrics API
        response = requests.get(
            f"{self.api_base_url}/metrics",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        self.assertEqual(response.status_code, 200)
        
        metrics = response.json()
        self.assertTrue(any(
            m['name'] == 'docker.container.cpu.usage' 
            for m in metrics
        ))
        
        # Cleanup
        container.remove(force=True)
        
        print("✓ Metric collection test passed")
    
    async def test_03_ml_predictions(self):
        """Test ML prediction functionality"""
        print("\nTesting ML predictions...")
        
        # Generate sample historical data
        dates = pd.date_range(
            start='2025-01-01',
            end='2025-01-07',
            freq='H'
        )
        data = pd.DataFrame({
            'value': [50 + 30 * (i.hour/24) + 10 * (i.dayofweek/7) 
                     for i in dates]
        }, index=dates)
        
        # Initialize optimizer and get predictions
        optimizer = ResourceOptimizer({
            'utilization_threshold_low': 20,
            'utilization_threshold_high': 80
        })
        
        predictions = optimizer.predict_utilization(data)
        
        self.assertIn('predictions', predictions)
        self.assertIn('recommended_actions', predictions)
        self.assertTrue(len(predictions['predictions']) > 0)
        
        print("✓ ML predictions test passed")
    
    async def test_04_automation(self):
        """Test automation functionality"""
        print("\nTesting automation...")
        
        scheduler = ResourceScheduler({
            'aws': {'enabled': True, 'region': self.aws_region}
        })
        
        # Schedule a test task
        task = scheduler.schedule_task({
            'resource_id': 'test-resource',
            'action': 'stop',
            'schedule_time': datetime.now() + timedelta(minutes=5),
            'parameters': {
                'provider': 'aws',
                'resource_type': 'ec2'
            }
        })
        
        self.assertTrue(task)
        
        # Verify task status
        status = scheduler.get_task_status('test-resource')
        self.assertTrue(len(status) > 0)
        self.assertEqual(status[0]['resource_id'], 'test-resource')
        
        print("✓ Automation test passed")
    
    async def test_05_api_integration(self):
        """Test API endpoints"""
        print("\nTesting API integration...")
        
        # Test health endpoint
        response = requests.get(f"{self.api_base_url}/health")
        self.assertEqual(response.status_code, 200)
        
        # Test metrics submission
        test_metric = {
            "name": "test.metric",
            "value": 42.0,
            "timestamp": datetime.now().timestamp(),
            "tags": {"host": "test-host"}
        }
        
        response = requests.post(
            f"{self.api_base_url}/metrics",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"metrics": [test_metric]}
        )
        self.assertEqual(response.status_code, 200)
        
        print("✓ API integration test passed")

    async def test_06_agent_installation_new(self):
        """Test agent installation process"""
        response = await self.client.post("/api/v1/agent/install", json={
            "resource_id": "test-instance",
            "resource_type": "ec2",
            "region": "us-east-1"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "agent_id" in data

    async def test_07_metric_collection_new(self):
        """Test metric collection and storage"""
        metrics = {
            "resource_id": "test-instance",
            "metrics": {
                "cpu_usage": 45.5,
                "memory_usage": 78.2,
                "network_usage": 25.8,
                "disk_usage": 62.1
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        response = await self.client.post("/api/v1/resources/metrics", json=metrics)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    async def test_08_ml_predictions_new(self):
        """Test ML predictions"""
        response = await self.client.get("/api/v1/resources/predictions/test-instance")
        assert response.status_code == 200
        data = response.json()
        assert "resource_id" in data
        assert "predictions" in data

    async def test_09_automation_new(self):
        """Test automation scheduling"""
        action = {
            "resource_id": "test-instance",
            "action": "stop",
            "scheduled_time": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
        response = await self.client.post("/api/v1/resources/schedule", json=action)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "scheduled"

    async def test_10_api_integration_new(self):
        """Test API integration"""
        # Test health endpoint
        response = await self.client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        # Test metrics endpoint
        metrics = {
            "resource_id": "test-instance",
            "metrics": {
                "cpu_usage": 55.5,
                "memory_usage": 68.2,
                "network_usage": 35.8,
                "disk_usage": 72.1
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        response = await self.client.post("/api/v1/resources/metrics", json=metrics)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # Test recommendations endpoint
        response = await self.client.get("/api/v1/resources/recommendations/test-instance")
        assert response.status_code == 200
        data = response.json()
        assert "resource_id" in data
        assert "recommendations" in data

@pytest.fixture
def setup():
    """Set up test environment"""
    client = TestClient(app)
    mock_dynamodb = mock_dynamodb()
    mock_s3 = mock_s3()
    mock_ec2 = mock_ec2()

    # Start mocks
    mock_dynamodb.start()
    mock_s3.start()
    mock_ec2.start()

    # Set up AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Create DynamoDB tables
    dynamodb = boto3.resource('dynamodb')
    
    # Create metrics table
    dynamodb.create_table(
        TableName='cloud_pioneer_metrics',
        KeySchema=[
            {'AttributeName': 'resource_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'resource_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Create schedules table
    dynamodb.create_table(
        TableName='cloud_pioneer_schedules',
        KeySchema=[
            {'AttributeName': 'resource_id', 'KeyType': 'HASH'},
            {'AttributeName': 'scheduled_time', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'resource_id', 'AttributeType': 'S'},
            {'AttributeName': 'scheduled_time', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    yield client

    # Stop mocks
    mock_dynamodb.stop()
    mock_s3.stop()
    mock_ec2.stop()

class CloudPioneerE2ETest:
    """End-to-end test suite for CloudPioneer"""

    def test_01_agent_installation(self, setup):
        """Test agent installation process"""
        with patch('src.agent.installer.AgentInstaller') as mock_installer:
            installer_instance = MagicMock()
            mock_installer.return_value = installer_instance
            installer_instance.install.return_value = True

            response = setup.post("/api/v1/agent/install", json={
                "instance_id": "i-1234567890abcdef0",
                "region": "us-east-1"
            })

            assert response.status_code == 200
            assert response.json()["status"] == "success"

    def test_02_metric_collection(self, setup):
        """Test metric collection process"""
        metrics = {
            "resource_id": "i-1234567890abcdef0",
            "metrics": {
                "cpu_utilization": 45.5,
                "memory_utilization": 78.2,
                "network_in": 1000000,
                "network_out": 2000000
            },
            "timestamp": "2025-01-24T14:20:20Z"
        }

        response = setup.post("/api/v1/resources/metrics", json=metrics)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_03_ml_predictions(self, setup):
        """Test ML predictions"""
        with patch('src.ml.resource_optimizer.ResourceOptimizer') as mock_optimizer:
            optimizer_instance = MagicMock()
            mock_optimizer.return_value = optimizer_instance
            optimizer_instance.predict_resource_usage.return_value = {
                "predictions": [
                    {"metric": "cpu_utilization", "value": 55.0, "confidence": 0.85},
                    {"metric": "memory_utilization", "value": 82.0, "confidence": 0.82}
                ]
            }

            response = setup.get("/api/v1/resources/predictions/i-1234567890abcdef0")
            assert response.status_code == 200
            assert "predictions" in response.json()

    def test_04_automation(self, setup):
        """Test automation workflows"""
        with patch('src.automation.scheduler.ResourceScheduler') as mock_scheduler:
            scheduler_instance = MagicMock()
            mock_scheduler.return_value = scheduler_instance
            scheduler_instance.schedule_task.return_value = True

            action = {
                "resource_id": "i-1234567890abcdef0",
                "action": "stop",
                "scheduled_time": "2025-01-24T15:20:20Z"
            }

            response = setup.post("/api/v1/resources/schedule", json=action)
            assert response.status_code == 200
            assert response.json()["status"] == "success"

    def test_05_api_integration(self, setup):
        """Test API integration"""
        # Test health check
        response = setup.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        # Test root endpoint
        response = setup.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_06_agent_installation_new(self, setup):
        """Test new agent installation process"""
        with patch('src.agent.installer.AgentInstaller') as mock_installer:
            installer_instance = MagicMock()
            mock_installer.return_value = installer_instance
            installer_instance.install.return_value = True

            response = setup.post("/api/v1/agent/install", json={
                "instance_id": "i-0987654321fedcba0",
                "region": "us-west-2"
            })

            assert response.status_code == 200
            assert response.json()["status"] == "success"

    def test_07_metric_collection_new(self, setup):
        """Test new metric collection process"""
        metrics = {
            "resource_id": "i-0987654321fedcba0",
            "metrics": {
                "cpu_utilization": 35.5,
                "memory_utilization": 68.2,
                "network_in": 800000,
                "network_out": 1500000
            },
            "timestamp": "2025-01-24T14:20:20Z"
        }

        response = setup.post("/api/v1/resources/metrics", json=metrics)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_08_ml_predictions_new(self, setup):
        """Test new ML predictions"""
        with patch('src.ml.resource_optimizer.ResourceOptimizer') as mock_optimizer:
            optimizer_instance = MagicMock()
            mock_optimizer.return_value = optimizer_instance
            optimizer_instance.predict_resource_usage.return_value = {
                "predictions": [
                    {"metric": "cpu_utilization", "value": 45.0, "confidence": 0.88},
                    {"metric": "memory_utilization", "value": 72.0, "confidence": 0.85}
                ]
            }

            response = setup.get("/api/v1/resources/predictions/i-0987654321fedcba0")
            assert response.status_code == 200
            assert "predictions" in response.json()

    def test_09_automation_new(self, setup):
        """Test new automation workflows"""
        with patch('src.automation.scheduler.ResourceScheduler') as mock_scheduler:
            scheduler_instance = MagicMock()
            mock_scheduler.return_value = scheduler_instance
            scheduler_instance.schedule_task.return_value = True

            action = {
                "resource_id": "i-0987654321fedcba0",
                "action": "start",
                "scheduled_time": "2025-01-24T16:20:20Z"
            }

            response = setup.post("/api/v1/resources/schedule", json=action)
            assert response.status_code == 200
            assert response.json()["status"] == "success"

    def test_10_api_integration_new(self, setup):
        """Test new API integration"""
        # Test metrics endpoint
        metrics = {
            "resource_id": "i-0987654321fedcba0",
            "metrics": {
                "cpu_utilization": 25.5,
                "memory_utilization": 58.2,
                "network_in": 600000,
                "network_out": 1200000
            },
            "timestamp": "2025-01-24T14:20:20Z"
        }

        response = setup.post("/api/v1/resources/metrics", json=metrics)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # Test recommendations endpoint
        response = setup.get("/api/v1/resources/recommendations/i-0987654321fedcba0")
        assert response.status_code == 200
        assert "recommendations" in response.json()

if __name__ == '__main__':
    unittest.main(verbosity=2)
