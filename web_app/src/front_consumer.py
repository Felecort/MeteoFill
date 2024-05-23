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

def get_channel(rabbitmq_user: str,
                rabbitmq_pass: str,
                rabbitmq_server_name: str,
                rabbitmq_queue: str,
                ) -> pika.adapters.blocking_connection.BlockingChannel:
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server_name, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue)
    
    return channel

