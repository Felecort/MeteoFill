
from src import app
from time import sleep
from multiprocessing import Process
from src import front_consumer
import os


RABBITMQ_LOCATION = os.environ["RABBITMQ_DEFAULT_LOCATION"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_DEFAULT_SERVER_NAME = os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]

SYSTEM_2_FRONTEND_QUEUE = os.environ["SYSTEM_2_FRONTEND"]


def run_web():
    app.run(host="0.0.0.0", debug=True)


def run_consumer():
    print("Waiting...")
    sleep(10)
    channel = front_consumer.get_channel(RABBITMQ_DEFAULT_USER,
                                        RABBITMQ_DEFAULT_PASS,
                                        RABBITMQ_DEFAULT_SERVER_NAME,
                                        SYSTEM_2_FRONTEND_QUEUE)

    channel.basic_consume(queue=SYSTEM_2_FRONTEND_QUEUE,
                            on_message_callback=front_consumer.callback,
                            auto_ack=True)
    print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_consumer)
    p2.start()
