import pika
import json
# from src import nans_handler
from src.nans_handler import fill_missing_values, create_nan, calculate_rmse
import pandas as pd
from datetime import datetime
from time import sleep
import os

name_mapping = {
    'temperature_2m': 'Температура',
    'relative_humidity_2m': 'Относительная влажность',
    'surface_pressure': 'Атмосферное давление',
    'wind_speed_10m': 'Скорость ветра',
    'wind_direction_10m': 'Направление ветра'
}

class BackConsumer:
    def __init__(self) -> None:
        pass

    def calculate_timestamps(self, start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
        timestamps = pd.date_range(
            start=start_timestamp,
            end=end_timestamp,
            # from nanoseconds to seconds
            freq=pd.Timedelta(int(delay * 1e9)),
            inclusive="both"
        )
        return timestamps


    def get_channel(self,
                    rabbitmq_user: str,
                    rabbitmq_pass: str,
                    rabbitmq_server_name: str,
                    rabbitmq_queue: str,
                    ) -> pika.adapters.blocking_connection.BlockingChannel:
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server_name, credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue=rabbitmq_queue)
        
        return channel


    def prepare_data(self, body):
        # from pprint import pprint
        json_data = json.loads(body)
        # pprint(json_data)
        # start_timestamp = datetime.fromisoformat(json_data["timestamps"]["start"])
        start_timestamp = datetime.strptime(json_data["timestamps"]["start"], "%Y-%m-%dT%H:%M:%S.%f000")
        # end_timestamp = datetime.fromisoformat(json_data["timestamps"]["end"])
        end_timestamp = datetime.strptime(json_data["timestamps"]["end"], "%Y-%m-%dT%H:%M:%S.%f000")
        delay = json_data["delay"]
        timestamps = self.calculate_timestamps(start_timestamp, end_timestamp, delay)

        data = {
            json_data["data"][i]["id"]: json_data["data"][i]["values"] for i in range(len(json_data["data"]))
        }
        data["date"] = timestamps


        df = pd.DataFrame(data)
        df.set_index("date", drop=True, inplace=True)
        return df


    def df_to_json_answer(self, df):
        answer = {}

        start = df.index[0].strftime('%Y-%m-%dT%H:%M')
        end = df.index[-1].strftime('%Y-%m-%dT%H:%M')
        delay = (df.index[1] - df.index[0]).total_seconds()

        answer["timestamps"] = {"start": start, "end": end}
        answer["delay"] = delay

        answer["data"] = [
            {"name": name_mapping[id],
            "id": id,
            "values": df[id].to_list()} for id in df.columns
        ]
        return answer


    # Define a callback function to process received messages
    def callback(self, ch, method, properties, body):
        print(" [X] BACK | Data received")
        df = self.prepare_data(body)
        df_filled_nans = fill_missing_values(df)

        answer = self.df_to_json_answer(df_filled_nans)

        self.send_data(answer)


    def send_data(self, data):
        # Connect to RabbitMQ server running on localhost
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["RABBITMQ_DEFAULT_SERVER_NAME"]))
        channel = connection.channel()

        # Declare a queue named 'data_queue'
        channel.queue_declare(queue=os.environ["BACKEND_2_SYSTEM"])

        json_string = json.dumps(data)
        channel.basic_publish(exchange='',
                            routing_key=os.environ["BACKEND_2_SYSTEM"],
                            body=json_string)
        print(" [X] BACK | Dataset Sent")

        connection.close()
