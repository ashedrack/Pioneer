"""Agent module."""

import json
import logging
import os
import threading
import time
from queue import Queue
from typing import Any, Dict, List, Optional

from .backends.base import BaseBackend
from .models import Metric


class BaseCollector:
    """Base collector class."""

    def __init__(self, agent_config: Dict[str, Any]):
        """Initialize collector."""
        self.config = agent_config
        self.logger = logging.getLogger(self.__class__.__name__)

    def collect(self) -> List[Metric]:
        """Collect metrics."""
        raise NotImplementedError


class MonitoringAgent:
    """Monitoring agent class."""

    def __init__(self, config_path: str):
        """Initialize agent."""
        self.config = self._load_config(config_path)
        self.collectors: Dict[str, BaseCollector] = {}
        self.metrics_queue = Queue()
        self.running = False
        self.logger = logging.getLogger("MonitoringAgent")

        # Initialize intervals from config
        agent_config = self.config.get("agent", {})
        self.collection_interval = agent_config.get("collection_interval", 60)
        self.shipping_interval = agent_config.get("shipping_interval", 10)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        with open(config_path, "r") as f:
            return json.load(f)

    def register_collector(self, name: str, collector: BaseCollector):
        """Register a collector."""
        self.collectors[name] = collector
        self.logger.info(f"Registered collector: {name}")

    def start(self):
        """Start the agent."""
        self.running = True
        collection_thread = threading.Thread(target=self._collection_loop)
        shipping_thread = threading.Thread(target=self._shipping_loop)

        collection_thread.start()
        shipping_thread.start()

        self.logger.info("Agent started")

    def stop(self):
        """Stop the agent."""
        self.running = False
        self.logger.info("Agent stopped")

    def _collection_loop(self):
        """Collection loop."""
        while self.running:
            try:
                for name, collector in self.collectors.items():
                    metrics = collector.collect()
                    for metric in metrics:
                        self.metrics_queue.put(metric)
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in collection loop: {e}")

    def _shipping_loop(self):
        """Shipping loop."""
        while self.running:
            try:
                metrics = []
                while not self.metrics_queue.empty():
                    metrics.append(self.metrics_queue.get())
                if metrics:
                    self._ship_metrics(metrics)
                time.sleep(self.shipping_interval)
            except Exception as e:
                self.logger.error(f"Error in shipping loop: {e}")

    def _ship_metrics(self, metrics: List[Metric]):
        """Ship metrics to backend."""
        self.logger.info(f"Shipping {len(metrics)} metrics")


class ResourceAgent:
    """Resource agent class."""

    def __init__(self, backend: BaseBackend):
        """Initialize agent."""
        self.backend = backend
        self.logger = logging.getLogger("ResourceAgent")

    async def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get resource by ID."""
        try:
            return await self.backend.get_resource(resource_id)
        except Exception as e:
            self.logger.error(f"Error getting resource {resource_id}: {e}")
            return None

    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all resources."""
        try:
            return await self.backend.list_resources()
        except Exception as e:
            self.logger.error(f"Error listing resources: {e}")
            return []

    async def start_resource(self, resource_id: str) -> bool:
        """Start a resource."""
        try:
            return await self.backend.start_resource(resource_id)
        except Exception as e:
            self.logger.error(f"Error starting resource {resource_id}: {e}")
            return False

    async def stop_resource(self, resource_id: str) -> bool:
        """Stop a resource."""
        try:
            return await self.backend.stop_resource(resource_id)
        except Exception as e:
            self.logger.error(f"Error stopping resource {resource_id}: {e}")
            return False
