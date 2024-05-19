#front_receiver.py
import pika
from time import sleep
import json
from src import json_pars

# Global variable to store the received JSON data
def callback(ch, method, properties, body):
    print(" [X] FRONT | Received JSON")
    
    new_data = body.decode('utf-8')
    new_data = json.loads(new_data)
    new_data_df = json_pars.parsing(new_data)
    
    with open("response.json", "r") as f:
        previous_data = json.load(f)
        previous_data_df = json_pars.parsing(previous_data)
    

    ### EXPERIMENTAL
    # FOR DEBUG PURPOSES ONLY
    with open("response.json", "w") as f:
        json.dump(new_data, f)
    ### MUST BE IN "response.json"
    # result = json_pars.update_data(new_data, previous_data)

def get_channel():
    # Connect to RabbitMQ server running on localhost
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    channel = connection.channel()

    # Declare a queue named 'data_queue'
    channel.queue_declare(queue='gui_queue')

    return channel

