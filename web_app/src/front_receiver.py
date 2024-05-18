#front_receiver.py
import pika
from time import sleep
import json


# Global variable to store the received JSON data
def callback(ch, method, properties, body):
    print(" [X] FRONT | Received JSON")
    
    # Decode the message and store it in the global variable
    json_data = body.decode('utf-8')
    # json.dumps(json_data)
    with open('actual_data.json', 'w') as f:
        f.write(json_data)
        print(" [X] FRONT | JSON Saved")


def get_channel():
    # Connect to RabbitMQ server running on localhost
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    channel = connection.channel()

    # Declare a queue named 'data_queue'
    channel.queue_declare(queue='gui_queue')

    return channel

