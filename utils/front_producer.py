import pika
import json


def send_data(name="response.json"):
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'system2frontend'
    channel.queue_declare(queue='system2frontend')

    # Sample dataset
    with open(f"utils/{name}", 'r') as f:
        dataset = json.load(f)

    # Convert dataset to JSON string and send it to the 'system2frontend'
    json_string = json.dumps(dataset)
    channel.basic_publish(exchange='',
                        routing_key='system2frontend',
                        body=json_string)
    print(" [X] FRONT | Dataset Sent")

    connection.close()


if __name__ == "__main__":
    send_data()
