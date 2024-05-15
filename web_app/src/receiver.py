import pika
import json
import pandas as pd
from datetime import datetime
from time import sleep
sleep(13)


def calculate_timestamps(start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
    timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        # from nanoseconds to seconds
        freq=pd.Timedelta(int(delay * 1e9)),
        inclusive="both"
    )
    return timestamps


# Connect to RabbitMQ server running on localhost
credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
channel = connection.channel()

# Declare a queue named 'gui_queue'
channel.queue_declare(queue='gui_queue')

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    raise ValueError
    print("callback")


# Consume messages from the 'gui_queue'
channel.basic_consume(queue='gui_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [x] Waiting for messages. To exit press CTRL+C')
#channel.start_consuming()
