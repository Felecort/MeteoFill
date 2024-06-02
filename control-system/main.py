from src import BusinessLogic
from time import sleep
import os

RABBITMQ_LOCATION = os.environ["RABBITMQ_DEFAULT_LOCATION"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_DEFAULT_SERVER_NAME = os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]

BACKEND_2_SYSTEM_QUEUE = os.environ["BACKEND_2_SYSTEM"]
SYSTEM_2_BACKEND_QUEUE = os.environ["SYSTEM_2_BACKEND"]
SYSTEM_2_FRONTEND_QUEUE = os.environ["SYSTEM_2_FRONTEND"]

REQUEST_FREQUENCY = 10


if __name__ == '__main__':
    sleep(12)
    bl = BusinessLogic(REQUEST_FREQUENCY,
                       SYSTEM_2_BACKEND_QUEUE,
                       SYSTEM_2_FRONTEND_QUEUE,
                       BACKEND_2_SYSTEM_QUEUE,
                       RABBITMQ_DEFAULT_SERVER_NAME,
                       RABBITMQ_DEFAULT_USER,
                       RABBITMQ_DEFAULT_PASS,
                       RABBITMQ_LOCATION)
    bl.run()