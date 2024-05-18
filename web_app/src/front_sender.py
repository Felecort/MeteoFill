import pika
import json

# Connect to RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue named 'gui_queue'
channel.queue_declare(queue='gui_queue')

# Sample dataset
with open('web_app/actual_data.json', 'r') as f:
    dataset = json.load(f)

# Convert dataset to JSON string and send it to the 'gui_queue'
json_string = json.dumps(dataset)
channel.basic_publish(exchange='',
                      routing_key='gui_queue',
                      body=json_string)
print(" [X] FRONT | Dataset Sent")

connection.close()
