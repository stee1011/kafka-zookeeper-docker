# kafka_producer.py
# This script acts as a Kafka producer, sending a series of messages to a specified topic.

import socket
from confluent_kafka import Producer
import time

# --- Configuration ---
# Update with your Kafka broker's address. If running Kafka locally via Docker,
# 'localhost:9092' is a common default.
KAFKA_BROKER = 'localhost:9092'
# The topic you want to send messages to.
KAFKA_TOPIC = 'my-first-topic'

def delivery_report(err, msg):
    """
    Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush().
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def main():
    """ Main function to initialize and run the Kafka producer. """
    # --- Producer Configuration ---
    # Here, we create a configuration dictionary for the producer.
    # 'bootstrap.servers' points to our Kafka cluster.
    # 'client.id' is an optional identifier for the client instance.
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': socket.gethostname()
    }

    # --- Create Producer instance ---
    # We instantiate the Producer with our configuration.
    producer = Producer(conf)

    print(f"Producer connected to {KAFKA_BROKER}. Sending messages to topic '{KAFKA_TOPIC}'.")
    print("Press Ctrl+C to exit.")

    try:
        # --- Message Production Loop ---
        # We send 10 messages, one per second.
        for i in range(10):
            message_key = f'key-{i + 10}'
            message_value = f'Hello from Python! This is message number {i+10}'

            # The produce() method is asynchronous. It sends the message and returns immediately.
            # The delivery_report callback will be called later to confirm delivery.
            producer.produce(
                KAFKA_TOPIC,
                key=message_key.encode('utf-8'),
                value=message_value.encode('utf-8'),
                callback=delivery_report
            )

            # poll() serves delivery reports from previous produce() calls.
            # It's important to call this periodically to serve the callbacks.
            producer.poll(0)

            print(f"Sent: Key='{message_key}', Value='{message_value}'")
            time.sleep(1) # Wait for 1 second before sending the next message

    except KeyboardInterrupt:
        print("Producer interrupted by user.")
    finally:
        # --- Flush and Cleanup ---
        # flush() waits for all outstanding messages to be delivered and delivery reports received.
        print("Flushing messages...")
        producer.flush()
        print("Producer shut down.")

if __name__ == '__main__':
    main()
