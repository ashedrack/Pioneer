from kafka import KafkaProducer
import json
from typing import Dict, Any, List
from ..agent import Metric

class MetricsProducer:
    def __init__(self, config: Dict[str, Any]):
        self.producer = KafkaProducer(
            bootstrap_servers=config['kafka_servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol="SSL" if config.get('use_ssl', True) else "PLAINTEXT",
            max_request_size=1342177280,  # Match broker setting (1.25GB)
            buffer_memory=2684354560,     # 2.5GB buffer
            compression_type='gzip',      # Add compression to help with large messages
            acks='all',                   # Ensure durability
            retries=3                     # Retry on temporary failures
        )
        self.topic = config['topic']

    def send_metrics(self, metrics: List[Metric]):
        for metric in metrics:
            self.producer.send(
                self.topic,
                {
                    'name': metric.name,
                    'value': metric.value,
                    'tags': metric.tags,
                    'timestamp': metric.timestamp,
                    'source': metric.source
                }
            )
        self.producer.flush()
