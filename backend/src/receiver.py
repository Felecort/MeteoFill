import pika
import json
import nans_handler
import pandas as pd
from datetime import datetime
from  nans_handler import fill_missing_values, create_nan, calculate_rmse
from time import sleep
sleep(7)


def calculate_timestamps(start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
    timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        # from nanoseconds to seconds
        freq=pd.Timedelta(int(delay * 1e9)),
        inclusive="both"
    )
    return timestamps


# # Function to be called with the received data
# def process_data(data):
#     print("Received Data:")
#     for person in data:
#         print(f"Name: {person['name']}, Age: {person['age']}")

# Connect to RabbitMQ server running on localhost
credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
channel = connection.channel()

# Declare a queue named 'data_queue'
channel.queue_declare(queue='data_queue')

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    json_data = json.loads(body)
    start_timestamp = datetime.fromisoformat(json_data["timestamps"]["start"])
    end_timestamp = datetime.fromisoformat(json_data["timestamps"]["end"])
    delay = json_data["delay"]
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)
    
    data = {
        json_data["data"][i]["id"]: json_data["data"][i]["values"] for i in range(len(json_data["data"]))
    }
    data["date"] = timestamps

    df = pd.DataFrame(data)
    df.set_index("date", drop=True, inplace=True)
    df_with_nans = create_nan(df)
    df_filled_nans = fill_missing_values(df_with_nans)
    print(f" [x] RMSE: {calculate_rmse(df, df_filled_nans)}")

    print(df_filled_nans)


# Consume messages from the 'data_queue'
channel.basic_consume(queue='data_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
