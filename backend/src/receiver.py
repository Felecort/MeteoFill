import pika
import json
from time import sleep
sleep(10)
# Function to be called with the received data
def process_data(data):
    print("Received Data:")
    for person in data:
        print(f"Name: {person['name']}, Age: {person['age']}")

# Connect to RabbitMQ server running on localhost
credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
channel = connection.channel()

# Declare a queue named 'data_queue'
channel.queue_declare(queue='data_queue')

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    data = json.loads(body)
    process_data(data)

# Consume messages from the 'data_queue'
channel.basic_consume(queue='data_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
