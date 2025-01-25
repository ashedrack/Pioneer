"""Test agent module."""
import pytest
from src.agent.backends.base import BaseBackend
from src.agent.agent import ResourceAgent

class TestBackend(BaseBackend):
    """Test backend implementation."""
    def __init__(self):
        """Initialize test backend."""
        self.resources = {
            'test-instance': {
                'id': 'test-instance',
                'state': 'running'
            }
        }

    async def get_resource(self, resource_id: str):
        """Get resource by ID."""
        return self.resources.get(resource_id)

    async def list_resources(self):
        """List all resources."""
        return list(self.resources.values())

    async def start_resource(self, resource_id: str):
        """Start a resource."""
        if resource_id in self.resources:
            self.resources[resource_id]['state'] = 'running'
            return True
        return False

    async def stop_resource(self, resource_id: str):
        """Stop a resource."""
        if resource_id in self.resources:
            self.resources[resource_id]['state'] = 'stopped'
            return True
        return False

@pytest.fixture
def backend():
    """Create test backend instance."""
    return TestBackend()

@pytest.fixture
def agent(backend):
    """Create agent instance."""
    return ResourceAgent(backend)

@pytest.mark.asyncio
async def test_get_resource(agent):
    """Test get_resource method."""
    resource = await agent.get_resource('test-instance')
    assert resource is not None
    assert resource['id'] == 'test-instance'
    assert resource['state'] == 'running'

@pytest.mark.asyncio
async def test_get_resource_not_found(agent):
    """Test get_resource method with non-existent resource."""
    resource = await agent.get_resource('non-existent')
    assert resource is None
