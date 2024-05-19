import pika
import json


def send_data(name="response_example.json"):
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'data_queue'
    channel.queue_declare(queue='data_queue')

    # Sample dataset
    with open(f"backend/{name}", 'r') as f:
        dataset = json.load(f)

    # Convert dataset to JSON and send it to the 'data_queue'
    json_string = json.dumps(dataset)
    channel.basic_publish(exchange='',
                        routing_key='data_queue',
                        body=json_string)
    print(" [X] BACK | Dataset Sent")

    connection.close()


if __name__ == "__main__":
    send_data()
