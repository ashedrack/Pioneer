"""
Enhanced resource metrics collector for detailed system monitoring.
"""
import psutil
import time
from typing import Dict, Any
import logging
from datetime import datetime
import asyncio

class ResourceMetricsCollector:
    """Collects system resource metrics."""

    def __init__(self, collection_interval: int = 60):
        """Initialize collector with interval."""
        self.collection_interval = collection_interval
        self.logger = logging.getLogger(__name__)

    def collect_metrics(self, resource_id: str = None) -> Dict[str, Any]:
        """Collect comprehensive system metrics."""
        try:
            cpu_metrics = self._collect_cpu_metrics()
            memory_metrics = self._collect_memory_metrics()
            disk_metrics = self._collect_disk_metrics()
            network_metrics = self._collect_network_metrics()

            return {
                'cpu_utilization': cpu_metrics['usage_percent'],
                'memory_utilization': memory_metrics['percent'],
                'disk_utilization': disk_metrics['partitions'].get('/', {}).get('percent', 0),
                'network_in': network_metrics['bytes_recv'],
                'network_out': network_metrics['bytes_sent']
            }
        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {str(e)}")
            raise

    def _collect_cpu_metrics(self) -> Dict[str, float]:
        """Collect detailed CPU metrics."""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'load_avg_1min': psutil.getloadavg()[0],
            'load_avg_5min': psutil.getloadavg()[1],
            'load_avg_15min': psutil.getloadavg()[2],
            'ctx_switches': psutil.cpu_stats().ctx_switches,
            'interrupts': psutil.cpu_stats().interrupts,
            'soft_interrupts': psutil.cpu_stats().soft_interrupts
        }

    def _collect_memory_metrics(self) -> Dict[str, float]:
        """Collect detailed memory metrics."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_free': swap.free,
            'swap_percent': swap.percent
        }

    def _collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect detailed disk metrics."""
        disk_usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except Exception as e:
                self.logger.warning(f"Could not collect disk metrics for {partition.mountpoint}: {str(e)}")
        
        io_counters = psutil.disk_io_counters()
        return {
            'partitions': disk_usage,
            'io_counters': {
                'read_bytes': io_counters.read_bytes,
                'write_bytes': io_counters.write_bytes,
                'read_count': io_counters.read_count,
                'write_count': io_counters.write_count,
                'read_time': io_counters.read_time,
                'write_time': io_counters.write_time
            }
        }

    def _collect_network_metrics(self) -> Dict[str, Any]:
        """Collect detailed network metrics."""
        net_counters = psutil.net_io_counters()
        return {
            'bytes_sent': net_counters.bytes_sent,
            'bytes_recv': net_counters.bytes_recv,
            'packets_sent': net_counters.packets_sent,
            'packets_recv': net_counters.packets_recv,
            'errin': net_counters.errin,
            'errout': net_counters.errout,
            'dropin': net_counters.dropin,
            'dropout': net_counters.dropout
        }

    async def start_collection(self):
        """Start continuous metric collection"""
        while True:
            try:
                metrics = self.collect_metrics()
                # Here you would typically send metrics to your data pipeline
                # For example, using Kafka or direct API calls
                
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in metric collection loop: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying
