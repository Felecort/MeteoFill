import pika
import json
# from src import nans_handler
from src.nans_handler import fill_missing_values, create_nan, calculate_rmse
import pandas as pd
from datetime import datetime
from time import sleep
sleep(10)


def calculate_timestamps(start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
    timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        # from nanoseconds to seconds
        freq=pd.Timedelta(int(delay * 1e9)),
        inclusive="both"
    )
    return timestamps


def get_channel(rabbitmq_user: str,
                rabbitmq_pass: str,
                rabbitmq_server_name: str,
                rabbitmq_queue: str,
                ) -> pika.adapters.blocking_connection.BlockingChannel:
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server_name, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue)
    
    return channel

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    print(" [X] BACK | HELLO FROM BACK")
    # json_data = json.loads(body)
    # start_timestamp = datetime.fromisoformat(json_data["timestamps"]["start"])
    # end_timestamp = datetime.fromisoformat(json_data["timestamps"]["end"])
    # delay = json_data["delay"]
    # timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)

    # data = {
    #     json_data["data"][i]["id"]: json_data["data"][i]["values"] for i in range(len(json_data["data"]))
    # }
    # data["date"] = timestamps

    # df = pd.DataFrame(data)
    # df.set_index("date", drop=True, inplace=True)
    # df_filled_nans = fill_missing_values(df)

    # print(f" [x] Dataset:")
    # print(df_filled_nans)



