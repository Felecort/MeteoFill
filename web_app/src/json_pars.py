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
    delay = data["delay"]
    try:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M:%S.%f000")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M:%S.%f000")
    except ValueError as ve:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M")
    
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

def update_data(data: pd.DataFrame, data_frame_presents: pd.DataFrame, max_rows=50) -> pd.DataFrame:
    result = pd.concat([data_frame_presents, data])
    result.reset_index(drop=True, inplace=True)
    result.sort_values("time", inplace=True)
    if len(result) >= max_rows:
        return result.loc[:max_rows]
    return result
