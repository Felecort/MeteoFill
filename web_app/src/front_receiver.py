import pika
import json
# import nans_handler
import pandas as pd
from datetime import datetime
# from  nans_handler import fill_missing_values, create_nan, calculate_rmse
from time import sleep
sleep(10)


# Connect to RabbitMQ server running on localhost
credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
channel = connection.channel()

# Declare a queue named 'data_queue'
channel.queue_declare(queue='gui_queue')

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    print(" [X] FRONT | HELLO FROM FRONT")


# Consume messages from the 'data_queue'
channel.basic_consume(queue='gui_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
