import pika
from time import sleep


def callback(ch, method, properties, body):
        print(" [X] FRONT | HELLO FROM FRONT")



def get_channel():
    # Connect to RabbitMQ server running on localhost
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    channel = connection.channel()

    # Declare a queue named 'data_queue'
    channel.queue_declare(queue='gui_queue')

    return channel

