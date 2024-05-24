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
    start_timestamp = datetime.fromisoformat(data["timestamps"]["start"])
    end_timestamp = datetime.fromisoformat(data["timestamps"]["end"])
    
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)
    
    df = pd.DataFrame({
        'time': timestamps,
        'temperature_before': data['data'][0]['values']['before'],
        'temperature_after': data['data'][0]['values']['after'],
        'wind_speed_before': data['data'][1]['values']['before'],
        'wind_speed_after': data['data'][1]['values']['after'],
        'wind_direction_before': data['data'][2]['values']['before'],
        'wind_direction_after': data['data'][2]['values']['after'],
        'pressure_before': data['data'][3]['values']['before'],
        'pressure_after': data['data'][3]['values']['after'],
        'humidity_before': data['data'][4]['values']['before'],
        'humidity_after': data['data'][4]['values']['after']
    })
    return df

def update_data(new_data: dict, max_rows=50):
    with open("response.json", "r") as f:
            previous_data = json.load(f)
            previous_data_df = parsing(previous_data)

    new_data_df = parsing(new_data)

    result = pd.concat([previous_data_df, new_data_df])
    result.reset_index(drop=True, inplace=True)
    #result.sort_values("time", inplace=True)
    if len(result) >= max_rows:
        result = result.iloc[:max_rows]

    # Конвертируем столбец времени в строковый формат "YYYY-MM-DDTHH:MM" перед сериализацией в JSON
    result['time'] = result['time'].dt.strftime('%Y-%m-%dT%H:%M')

    data_to_save = {
            "timestamps": {
                "start": result['time'].iloc[0],
                "end": result['time'].iloc[-1]
            },
            "delay": new_data["delay"],
            "data": [
                {
                    "name": "Температура",
                    "id": "temperature_2m",
                    "values": {
                        "before": result['temperature_before'].tolist(),
                        "after": result['temperature_after'].tolist()
                    }
                },
                {
                    "name": "Скорость ветра",
                    "id": "wind_speed_10m",
                    "values": {
                        "before": result['wind_speed_before'].tolist(),
                        "after": result['wind_speed_after'].tolist()
                    }
                },
                {
                    "name": "Направление ветра",
                    "id": "wind_direction_10m",
                    "values": {
                        "before": result['wind_direction_before'].tolist(),
                        "after": result['wind_direction_after'].tolist()
                    }
                },
                {
                    "name": "Давление",
                    "id": "pressure_msl",
                    "values": {
                        "before": result['pressure_before'].tolist(),
                        "after": result['pressure_after'].tolist()
                    }
                },
                {
                    "name": "Влажность",
                    "id": "humidity_2m",
                    "values": {
                        "before": result['humidity_before'].tolist(),
                        "after": result['humidity_after'].tolist()
                    }
                }
            ]
        }

    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)