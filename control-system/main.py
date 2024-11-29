from src import BusinessLogic
from time import sleep
import os
import requests


# Function to test connection
def check_connection(ip):
    try:
        # Sending a GET request with a timeout
        requests.get(f"http://{ip}:8092/", timeout=5)
        return ip
    except requests.exceptions.RequestException as e:
        # Handle exceptions gracefully
        return None


def get_current_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    tmp_ip = s.getsockname()[0]
    s.close()
    print(tmp_ip)
    return tmp_ip

IPS = [
    "localhost", 
    "host.docker.internal",
    "127.0.0.1",
    '192.168.199.111',
    get_current_ip(),
]

results = [valid_ip for ip in IPS if (valid_ip := check_connection(ip)) is not None]
ip_address = results[0]
# ip_address = '192.168.199.111'

RABBITMQ_LOCATION = os.environ["RABBITMQ_DEFAULT_LOCATION"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_DEFAULT_SERVER_NAME = os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]

BACKEND_2_SYSTEM_QUEUE = os.environ["BACKEND_2_SYSTEM"]
SYSTEM_2_BACKEND_QUEUE = os.environ["SYSTEM_2_BACKEND"]
SYSTEM_2_FRONTEND_QUEUE = os.environ["SYSTEM_2_FRONTEND"]

REQUEST_FREQUENCY = int(os.environ["REQUEST_FREQUENCY"])

try:
    METEOSTATION_LOCATION = os.environ["METEOSTATION_LOCATION"]
except KeyError:
    METEOSTATION_LOCATION = 'http://' + ip_address + ':8092/process-csv'


try:
    EXTERNAL_LOCATION = os.environ["EXTERNAL_LOCATION"]
except KeyError:
    EXTERNAL_LOCATION = 'http://' + ip_address + ':8092/rmse'
    

if __name__ == '__main__':
    sleep(12)
    bl = BusinessLogic(
        METEOSTATION_LOCATION,
        EXTERNAL_LOCATION,
        REQUEST_FREQUENCY,
        SYSTEM_2_BACKEND_QUEUE,
        SYSTEM_2_FRONTEND_QUEUE,
        BACKEND_2_SYSTEM_QUEUE,
        RABBITMQ_DEFAULT_SERVER_NAME,
        RABBITMQ_DEFAULT_USER,
        RABBITMQ_DEFAULT_PASS,
        RABBITMQ_LOCATION
    )
    bl.run()