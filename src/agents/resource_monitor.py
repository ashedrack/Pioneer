import psutil
import time
from datetime import datetime
import logging
from typing import Dict, Any

class ResourceMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "usage_percent": disk.percent
                }
            }
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {str(e)}")
            return None
    
    def get_process_metrics(self) -> Dict[str, Any]:
        """Collect metrics for running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "processes": processes
            }
        except Exception as e:
            self.logger.error(f"Error collecting process metrics: {str(e)}")
            return None
    
    def monitor(self, interval: int = 60) -> None:
        """Continuous monitoring with specified interval."""
        try:
            while True:
                metrics = self.get_system_metrics()
                if metrics:
                    # TODO: Implement metrics storage/transmission
                    self.logger.info(f"Collected metrics: {metrics}")
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Monitoring error: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor = ResourceMonitor()
    monitor.monitor()
