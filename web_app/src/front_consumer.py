import pika
import json
from src import json_pars

class FrontReceiver:
    def __init__(self, rabbitmq_user, rabbitmq_pass, rabbitmq_server_name, rabbitmq_queue):
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass
        self.rabbitmq_server_name = rabbitmq_server_name
        self.rabbitmq_queue = rabbitmq_queue
        self.channel = self.get_channel()

    def get_channel(self):
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_server_name, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=self.rabbitmq_queue)
        return channel

    def callback(self, ch, method, properties, body):
        print(" [X] FRONT | Received JSON")

        try:
            new_data = body.decode('utf-8')
            new_data = json.loads(new_data)
            json_pars.update_data(new_data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def start_consuming(self):
        self.channel.basic_consume(queue=self.rabbitmq_queue,
                                   on_message_callback=self.callback,
                                   auto_ack=True)
        print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()