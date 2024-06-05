import pandas as pd
import json
from datetime import datetime


# Функция для расчета временных меток
def calculate_timestamps(start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
    timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        # from nanoseconds to seconds
        freq=pd.Timedelta(int(delay * 1e9)),
        inclusive="both"
    )
    return timestamps

def parsing(data: dict) -> pd.DataFrame:
    delay = data["delay"]
    try:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M:%S.%f000")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M:%S.%f000")
    except ValueError as ve:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M")
    
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)

    data_before = {
        data["data"][i]["id"]+"_before": data["data"][i]["values"]["before"] for i in range(len(data["data"]))
    }

    data_after = {
        data["data"][i]["id"]+"_after": data["data"][i]["values"]["after"] for i in range(len(data["data"]))
    }

    data_time = {
        "time": timestamps
    }

    df_before = pd.DataFrame(data_before)
    df_after = pd.DataFrame(data_after)
    df_time = pd.DataFrame(data_time)

    df = pd.concat([df_time, df_before, df_after],axis=1)
    print(df)

    return df

def add_data(new_data: dict, max_rows=100):
    df = parsing(new_data)
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]

    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M')

    data_to_save = {
            "timestamps": {
                "start": df['time'].iloc[0],
                "end": df['time'].iloc[-1]
            },
            "delay": new_data["delay"],
            "data": [
                {
                    "name": "Температура",
                    "id": "temperature_2m",
                    "values": {
                        "before": df['temperature_2m_before'].tolist(),
                        "after": df['temperature_2m_after'].tolist()
                    }
                },
                {
                    "name": "Относительная влажность",
                    "id": "relative_humidity_2m",
                    "values": {
                        "before": df['relative_humidity_2m_before'].tolist(),
                        "after": df['relative_humidity_2m_after'].tolist()
                    }
                },
                {
                    "name": "Атмосферное давление",
                    "id": "surface_pressure",
                    "values": {
                        "before": df['surface_pressure_before'].tolist(),
                        "after": df['surface_pressure_after'].tolist()
                    }
                },
                {
                    "name": "Скорость ветра",
                    "id": "wind_speed_10m",
                    "values": {
                        "before": df['wind_speed_10m_before'].tolist(),
                        "after": df['wind_speed_10m_after'].tolist()
                    }
                },
                {
                    "name": "Направление ветра",
                    "id": "wind_direction_10m",
                    "values": {
                        "before": df['wind_direction_10m_before'].tolist(),
                        "after": df['wind_direction_10m_after'].tolist()
                    }
                }
            ]
        }

    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

def update_data(new_data: dict, max_rows=100):
    with open("response.json", "r") as f:
            previous_data = json.load(f)
            previous_data_df = parsing(previous_data)

    new_data_df = parsing(new_data)

    df = pd.concat([previous_data_df, new_data_df])
    df.reset_index(drop=True, inplace=True)
    #result.sort_values("time", inplace=True)
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]

    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M')

    data_to_save = {
            "timestamps": {
                "start": df['time'].iloc[0],
                "end": df['time'].iloc[-1]
            },
            "delay": new_data["delay"],
            "data": [
                {
                    "name": "Температура",
                    "id": "temperature_2m",
                    "values": {
                        "before": df['temperature_2m_before'].tolist(),
                        "after": df['temperature_2m_after'].tolist()
                    }
                },
                {
                    "name": "Относительная влажность",
                    "id": "relative_humidity_2m",
                    "values": {
                        "before": df['relative_humidity_2m_before'].tolist(),
                        "after": df['relative_humidity_2m_after'].tolist()
                    }
                },
                {
                    "name": "Атмосферное давление",
                    "id": "surface_pressure",
                    "values": {
                        "before": df['surface_pressure_before'].tolist(),
                        "after": df['surface_pressure_after'].tolist()
                    }
                },
                {
                    "name": "Скорость ветра",
                    "id": "wind_speed_10m",
                    "values": {
                        "before": df['wind_speed_10m_before'].tolist(),
                        "after": df['wind_speed_10m_after'].tolist()
                    }
                },
                {
                    "name": "Направление ветра",
                    "id": "wind_direction_10m",
                    "values": {
                        "before": df['wind_direction_10m_before'].tolist(),
                        "after": df['wind_direction_10m_after'].tolist()
                    }
                }
            ]
        }

    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)