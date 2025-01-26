import json
from typing import Any, Dict, List

from kafka import KafkaProducer

from ..agent import Metric


class MetricsProducer:
    def __init__(self, config: Dict[str, Any]):
        self.producer = KafkaProducer(
            bootstrap_servers=config["kafka_servers"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            security_protocol="SSL" if config.get("use_ssl", True) else "PLAINTEXT",
        )
        self.topic = config["topic"]

    def send_metrics(self, metrics: List[Metric]):
        for metric in metrics:
            self.producer.send(
                self.topic,
                {
                    "name": metric.name,
                    "value": metric.value,
                    "tags": metric.tags,
                    "timestamp": metric.timestamp,
                    "source": metric.source,
                },
            )
        self.producer.flush()
