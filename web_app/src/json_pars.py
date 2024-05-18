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

def update_data(data: pd.DataFrame, data_frame_presents: pd.DataFrame) -> pd.DataFrame:
    max_rows = 50
    df = data
    result = pd.concat([data_frame_presents, df])
    result = result.reset_index(drop=True)
    if (len(result)>=max_rows):
        result=result.drop(index=range(len(result)-max_rows))
    result = result.reset_index(drop=True)
    #print (result)
    return result
