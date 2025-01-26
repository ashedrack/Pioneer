"""Base backend classes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models import Metric


class MetricBackend(ABC):
    """Base metric backend class."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize backend."""
        self.config = config

    @abstractmethod
    def send_metrics(self, metrics: List[Metric]):
        """Send metrics to backend."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check backend health."""
        pass


class BaseBackend(ABC):
    """Base resource backend class."""

    @abstractmethod
    async def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """Get resource by ID."""
        pass

    @abstractmethod
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all resources."""
        pass

    @abstractmethod
    async def start_resource(self, resource_id: str) -> bool:
        """Start a resource."""
        pass

    @abstractmethod
    async def stop_resource(self, resource_id: str) -> bool:
        """Stop a resource."""
        pass
