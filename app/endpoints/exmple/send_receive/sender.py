import pika
import json

# Connect to RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue named 'data_queue'
channel.queue_declare(queue='data_queue')

# Sample dataset
dataset = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Convert dataset to JSON and send it to the 'data_queue'
channel.basic_publish(exchange='',
                      routing_key='data_queue',
                      body=json.dumps(dataset))
print(" [x] Dataset Sent")

connection.close()
