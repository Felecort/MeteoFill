import pika
import json

# Connect to RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue named 'data_queue'
channel.queue_declare(queue='data_queue')

# Sample dataset
import os
os.system("pwd")
with open('/home/vadim/projects/MeteoFill/backend/src/responce_example.json', 'r') as f:
    dataset = json.load(f)

# Convert dataset to JSON and send it to the 'data_queue'
channel.basic_publish(exchange='',
                      routing_key='data_queue',
                      body=json.dumps(dataset))
print(" [X] BACK | Dataset Sent")

connection.close()
