from src.web import WeatherApp
from time import sleep
from multiprocessing import Process
from src.front_consumer import FrontReceiver
import os

RABBITMQ_LOCATION = os.environ["RABBITMQ_DEFAULT_LOCATION"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_DEFAULT_SERVER_NAME = os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]
SYSTEM_2_FRONTEND_QUEUE = os.environ["SYSTEM_2_FRONTEND"]

def run_web():
    weather_app = WeatherApp()
    weather_app.run()

def run_consumer():
    print("Waiting...")
    sleep(10)
    receiver = FrontReceiver(RABBITMQ_DEFAULT_USER,
                             RABBITMQ_DEFAULT_PASS,
                             RABBITMQ_DEFAULT_SERVER_NAME,
                             SYSTEM_2_FRONTEND_QUEUE)
    receiver.start_consuming()

if __name__ == "__main__":
    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_consumer)
    p2.start()
