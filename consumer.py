import time 
from confluent_kafka import Consumer, KafkaException

KAFKA_TOPIC = 'my-first-topic'
GROUP_ID = 'my-consumer-group'
OFFSET = 'latest'
KAFKA_BROKER='localhost:9092'

conf = {
    'bootstrap.servers':KAFKA_BROKER,
    'group.id':GROUP_ID,
    'auto.offset.reset':OFFSET
}

consumer = Consumer(conf)
print(f"Listening to topic '{KAFKA_TOPIC}' on broker '{KAFKA_BROKER}'...")
consumer.subscribe([KAFKA_TOPIC])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print("A message Error found!")
            continue

        print(f"The message received is {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    print("Keyboad Interrupt Bye!")
finally:
    consumer.close()

    