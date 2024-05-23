
from src import back_consumer
import os

RABBITMQ_LOCATION = os.environ["RABBITMQ_DEFAULT_LOCATION"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_DEFAULT_SERVER_NAME = os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]

# BACKEND_2_SYSTEM = os.environ["BACKEND_2_SYSTEM"]
SYSTEM_2_BACKEND_QUEUE = os.environ["SYSTEM_2_BACKEND"]


if __name__ == "__main__":
    channel = back_consumer.get_channel(RABBITMQ_DEFAULT_USER,
                                        RABBITMQ_DEFAULT_PASS,
                                        RABBITMQ_DEFAULT_SERVER_NAME,
                                        SYSTEM_2_BACKEND_QUEUE)
    # Consume messages from the 'data_queue'
    channel.basic_consume(queue=SYSTEM_2_BACKEND_QUEUE,
                        on_message_callback=back_consumer.callback,
                        auto_ack=True)

    print(' [x] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()