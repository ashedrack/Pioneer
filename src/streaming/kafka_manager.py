"""
Kafka manager for handling real-time data streaming.
"""
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
from typing import Dict, Any, Callable, Optional
import json
import logging

class KafkaManager:
    def __init__(self, bootstrap_servers: str, client_id: str, testing: bool = False):
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self.testing = testing
        self.logger = logging.getLogger(__name__)
        self.producer = None
        
        if not testing:
            try:
                self.producer = self._create_producer()
            except NoBrokersAvailable:
                self.logger.warning("No Kafka brokers available. Running in degraded mode.")
            except Exception as e:
                self.logger.error(f"Failed to create Kafka producer: {str(e)}")
        self.consumers = {}

    def _create_producer(self) -> Optional[KafkaProducer]:
        """Create Kafka producer with default settings"""
        try:
            return KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=self.client_id,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1,
                max_request_size=1342177280,  # Match broker setting (1.25GB)
                buffer_memory=2684354560,     # 2.5GB buffer
                compression_type='gzip'       # Add compression to help with large messages
            )
        except Exception as e:
            self.logger.error(f"Failed to create Kafka producer: {str(e)}")
            return None

    def create_consumer(self, topic: str, group_id: str) -> KafkaConsumer:
        """Create a Kafka consumer for a specific topic"""
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            self.consumers[topic] = consumer
            return consumer
        except Exception as e:
            self.logger.error(f"Failed to create consumer for topic {topic}: {str(e)}")
            raise

    def send_message(self, topic: str, message: Dict[str, Any]) -> bool:
        """Send message to specified Kafka topic"""
        if self.testing:
            self.logger.info(f"[TEST MODE] Would send to {topic}: {message}")
            return True
            
        if not self.producer:
            self.logger.warning(f"No Kafka producer available. Message to {topic} not sent.")
            return False

        try:
            future = self.producer.send(topic, value=message)
            self.producer.flush()
            future.get(timeout=10)
            self.logger.debug(f"Message sent to topic {topic}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message to topic {topic}: {str(e)}")
            return False

    def consume_messages(self, topic: str, handler: Callable[[Dict[str, Any]], None]):
        """Consume messages from specified topic with a handler function"""
        if topic not in self.consumers:
            self.create_consumer(topic, f"{self.client_id}-{topic}-group")
        
        consumer = self.consumers[topic]
        try:
            for message in consumer:
                handler(message.value)
        except Exception as e:
            self.logger.error(f"Error consuming messages from topic {topic}: {str(e)}")
            raise

    def close(self):
        """Close all Kafka connections"""
        if self.producer and not self.testing:
            try:
                self.producer.close()
            except Exception as e:
                self.logger.error(f"Failed to close Kafka producer: {str(e)}")
        for consumer in self.consumers.values():
            consumer.close()
