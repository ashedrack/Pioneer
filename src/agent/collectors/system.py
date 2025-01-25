import psutil
import platform
from typing import Dict, List, Any
from ..agent import BaseCollector, Metric

class SystemMetricsCollector(BaseCollector):
    def collect(self) -> List[Metric]:
        metrics = []
        timestamp = time.time()
        
        # CPU Metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(Metric(
            name="system.cpu.utilization",
            value=cpu_percent,
            tags={"host": platform.node()},
            timestamp=timestamp,
            source="system"
        ))
        
        # Memory Metrics
        memory = psutil.virtual_memory()
        metrics.append(Metric(
            name="system.memory.used",
            value=memory.used,
            tags={"host": platform.node()},
            timestamp=timestamp,
            source="system"
        ))
        
        # Disk Metrics
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                metrics.append(Metric(
                    name="system.disk.used",
                    value=usage.used,
                    tags={
                        "host": platform.node(),
                        "device": partition.device,
                        "mountpoint": partition.mountpoint
                    },
                    timestamp=timestamp,
                    source="system"
                ))
            except Exception:
                continue
                
        return metrics
