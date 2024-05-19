import pika
import json


def send_data(name="response_example.json"):
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'gui_queue'
    channel.queue_declare(queue='gui_queue')

    # Sample dataset
    with open(f"utils/{name}", 'r') as f:
        dataset = json.load(f)

    # Convert dataset to JSON string and send it to the 'gui_queue'
    json_string = json.dumps(dataset)
    channel.basic_publish(exchange='',
                        routing_key='gui_queue',
                        body=json_string)
    print(" [X] FRONT | Dataset Sent")

    connection.close()


if __name__ == "__main__":
    send_data()
