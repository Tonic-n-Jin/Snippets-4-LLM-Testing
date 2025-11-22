import json
import logging
import time
from confluent_kafka import Producer
from pydantic import BaseModel, Field
from uuid import uuid4

# ---
# This example shows the PRODUCER side of event streaming.
# This class would be used inside an application (e.g., a FastAPI API)
# to generate business events ("user_signed_up", "item_added_to_cart").
# ---

logging.basicConfig(level=logging.INFO)

class EventProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        """Initializes the Kafka Producer."""
        config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'my-app-producer'
        }
        self.producer = Producer(config)
        self.topic = 'application_events'

    def delivery_report(self, err, msg):
        """Asynchronous callback for message delivery status."""
        if err is not None:
            logging.error(f"Message delivery failed: {err}")
        else:
            logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def produce_event(self, event_type: str, user_id: str, payload: dict):
        """
        Creates, serializes, and sends a standard event to Kafka.
        
        :param event_type: The name of the event (e.g., 'user_signup')
        :param user_id: The user associated with the event
        :param payload: A dictionary of event-specific data
        """
        event = {
            'event_id': str(uuid4()),
            'event_type': event_type,
            'user_id': user_id,
            'timestamp': int(time.time() * 1000), # Millisecond timestamp
            'payload': payload
        }
        
        try:
            # Send the message asynchronously.
            # The key (user_id) ensures all events for a user go to the same partition.
            self.producer.produce(
                self.topic,
                key=user_id.encode('utf-8'),
                value=json.dumps(event).encode('utf-8'),
                callback=self.delivery_report
            )
            # poll(0) is non-blocking and triggers callback delivery
            self.producer.poll(0)
            
        except BufferError:
            logging.error("Local producer queue is full. Flushing...")
            self.producer.flush(5) # Wait up to 5s
            # Retry producing
            self.producer.produce(
                self.topic,
                key=user_id.encode('utf-8'),
                value=json.dumps(event).encode('utf-8'),
                callback=self.delivery_report
            )
        except Exception as e:
            logging.error(f"Failed to produce event: {e}")

    def shutdown(self):
        """Flush all outstanding messages before shutting down."""
        logging.info("Flushing remaining messages...")
        self.producer.flush()


# --- Example Usage (e.g., inside your web application) ---
if __name__ == "__main__":
    producer = EventProducer()
    
    try:
        # Simulate an event
        signup_data = {'username': 'jdoe', 'email': 'jdoe@example.com'}
        producer.produce_event(
            event_type='user_signup', 
            user_id='u-12345', 
            payload=signup_data
        )
        
        # Simulate another event
        cart_data = {'item_id': 'item-abc', 'quantity': 2}
        producer.produce_event(
            event_type='add_to_cart',
            user_id='u-12345',
            payload=cart_data
        )
    finally:
        # Ensure all messages are sent before exiting
        producer.shutdown()
