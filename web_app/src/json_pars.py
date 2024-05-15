import pandas as pd
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
    delay = data[0]["delay"]
    start_timestamp = datetime.fromisoformat(data[0]["timestamps"]["start"])
    end_timestamp = datetime.fromisoformat(data[0]["timestamps"]["end"])
    
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)
    
    df = pd.DataFrame({
        'time': timestamps,
        'temperature_before': data[0]['data'][0]['values']['before'],
        'temperature_after': data[0]['data'][0]['values']['after'],
        'wind_speed_before': data[0]['data'][1]['values']['before'],
        'wind_speed_after': data[0]['data'][1]['values']['after'],
        'wind_direction_before': data[0]['data'][2]['values']['before'],
        'wind_direction_after': data[0]['data'][2]['values']['after'],
        'pressure_before': data[0]['data'][3]['values']['before'],
        'pressure_after': data[0]['data'][3]['values']['after'],
        'humidity_before': data[0]['data'][4]['values']['before'],
        'humidity_after': data[0]['data'][4]['values']['after']
    })
    return df

#def update_data()
