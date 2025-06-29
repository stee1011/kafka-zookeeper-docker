import socket 
import asyncio 
import time
import json
from confluent_kafka import Producer

KAFKA_TOPIC='my-first-topic'
KAFKA_BROKER='localhost:9092'

def derivery(err, msg):
    try:
        if not err:
            print(f"Message derivered Successful: Details: {msg.topic()} : [{msg.partition()}]")
        else:
            print("Error in derivery")
    except Exception as e:
        print(f"This exception occired: {e}")

conf = {
    'client.id' : socket.gethostname(),
    'bootstrap.servers' : KAFKA_BROKER
}

producer = Producer(conf)

messages_dict = {
    "user1": ["Clicked ad A", "Completed purchase"],
    "user2": ["Clicked ad B", "Logged out"],
    "user3": ["Logged in", "Viewed product X"],
    "user4": ["Added item to cart", "Viewed product Y"],
    "user5": ["Started checkout", "Removed item from cart"],
    "user6": ["Clicked email link", "Logged in"],
    "user7": ["Viewed homepage", "Browsed category Electronics"],
    "user8": ["Searched for headphones", "Viewed product Z"],
    "user9": ["Clicked ad C", "Signed up for newsletter"],
    "user10": ["Shared product on social media", "Logged out"],
    "user11": ["Logged in", "Checked order history"],
    "user12": ["Added shipping address", "Applied discount code"],
    "user13": ["Removed item from wishlist", "Browsed new arrivals"],
    "user14": ["Viewed sale page", "Started checkout"],
    "user15": ["Viewed product Y", "Watched demo video"],
    "user16": ["Created account", "Completed profile setup"],
    "user17": ["Opened mobile app", "Enabled notifications"],
    "user18": ["Reviewed product", "Rated 5 stars"],
    "user19": ["Logged out", "Logged back in"],
    "user20": ["Clicked push notification", "Completed purchase"]
}


try:
    for key, value in messages_dict.items():
        producer.produce(
            KAFKA_TOPIC,
            key=key.encode('utf-8'),
            value=json.dumps(value).encode('utf-8'),
            callback=derivery
    )
        producer.poll(0)
        time.sleep(2)

    

except KeyboardInterrupt:
    print("Bye!")

finally:
    producer.flush()
