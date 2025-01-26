import time
from typing import Any, Dict, List

import docker

from ..agent import BaseCollector, Metric


class DockerCollector(BaseCollector):
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(agent_config)
        self.docker_client = docker.from_env()
        self.container_include = agent_config.get("docker", {}).get(
            "include_containers", []
        )
        self.container_exclude = agent_config.get("docker", {}).get(
            "exclude_containers", []
        )

    def collect(self) -> List[Metric]:
        metrics = []
        timestamp = time.time()

        try:
            # Collect container metrics
            containers = self.docker_client.containers.list()

            for container in containers:
                # Skip if container should be excluded
                if self.container_exclude and container.name in self.container_exclude:
                    continue

                # Skip if we have an include list and container is not in it
                if (
                    self.container_include
                    and container.name not in self.container_include
                ):
                    continue

                # Get container stats
                stats = container.stats(stream=False)

                # CPU metrics
                cpu_delta = (
                    stats["cpu_stats"]["cpu_usage"]["total_usage"]
                    - stats["precpu_stats"]["cpu_usage"]["total_usage"]
                )
                system_delta = (
                    stats["cpu_stats"]["system_cpu_usage"]
                    - stats["precpu_stats"]["system_cpu_usage"]
                )

                if system_delta > 0:
                    cpu_percent = (cpu_delta / system_delta) * 100.0
                else:
                    cpu_percent = 0.0

                metrics.append(
                    Metric(
                        name="docker.cpu.usage_percent",
                        value=cpu_percent,
                        tags={
                            "container_name": container.name,
                            "image": (
                                container.image.tags[0]
                                if container.image.tags
                                else "unknown"
                            ),
                        },
                        timestamp=timestamp,
                        source="docker",
                    )
                )

                # Memory metrics
                memory_stats = stats["memory_stats"]
                memory_usage = memory_stats.get("usage", 0)
                memory_limit = memory_stats.get("limit", 0)

                if memory_limit > 0:
                    memory_percent = (memory_usage / memory_limit) * 100.0
                else:
                    memory_percent = 0.0

                metrics.append(
                    Metric(
                        name="docker.memory.usage_bytes",
                        value=memory_usage,
                        tags={
                            "container_name": container.name,
                            "image": (
                                container.image.tags[0]
                                if container.image.tags
                                else "unknown"
                            ),
                        },
                        timestamp=timestamp,
                        source="docker",
                    )
                )

                metrics.append(
                    Metric(
                        name="docker.memory.usage_percent",
                        value=memory_percent,
                        tags={
                            "container_name": container.name,
                            "image": (
                                container.image.tags[0]
                                if container.image.tags
                                else "unknown"
                            ),
                        },
                        timestamp=timestamp,
                        source="docker",
                    )
                )

                # Network metrics
                networks = stats["networks"]
                for interface, net_stats in networks.items():
                    metrics.extend(
                        [
                            Metric(
                                name="docker.network.rx_bytes",
                                value=net_stats["rx_bytes"],
                                tags={
                                    "container_name": container.name,
                                    "interface": interface,
                                    "image": (
                                        container.image.tags[0]
                                        if container.image.tags
                                        else "unknown"
                                    ),
                                },
                                timestamp=timestamp,
                                source="docker",
                            ),
                            Metric(
                                name="docker.network.tx_bytes",
                                value=net_stats["tx_bytes"],
                                tags={
                                    "container_name": container.name,
                                    "interface": interface,
                                    "image": (
                                        container.image.tags[0]
                                        if container.image.tags
                                        else "unknown"
                                    ),
                                },
                                timestamp=timestamp,
                                source="docker",
                            ),
                        ]
                    )

        except Exception as e:
            self.logger.error(f"Error collecting Docker metrics: {e}")

        return metrics
