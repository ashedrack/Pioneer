"""Agent models."""
from typing import Dict, Any

class Metric:
    """Metric model."""
    def __init__(self, name: str, value: float, tags: Dict[str, Any] = None):
        """Initialize metric."""
        self.name = name
        self.value = value
        self.tags = tags or {}
