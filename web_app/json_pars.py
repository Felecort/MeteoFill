import pandas as pd
from datetime import datetime, timedelta
import json

# Загрузка JSON
#with open('Шаблон_ответа_на_запрос_данных_для_визуализации.json', 'r') as f:
#    data = json.load(f)

# Функция для расчета временных меток
def calculate_timestamps(start_timestamp, end_timestamp, delay):
    timestamps = []
    current_timestamp = start_timestamp
    while current_timestamp <= end_timestamp:
        timestamps.append(current_timestamp)
        current_timestamp += timedelta(seconds=delay)
    return timestamps


def parsing (data):

    # Задержка между временными метками
    delay = data[0]["delay"]

    # Начальная и конечная временные метки
    start_timestamp = datetime.fromisoformat(data[0]["timestamps"]["start"])
    end_timestamp = datetime.fromisoformat(data[0]["timestamps"]["end"])

    # Расчет временных меток
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)

    # Создание пустого DataFrame
    df = pd.DataFrame(columns=['time', 'temperature_before', 'temperature_after', 'wind_speed_before', 'wind_speed_after', 'wind_direction_before','wind_direction_after','pressure_before','pressure_after','humidity_before','humidity_after'])

    # Заполнение DataFrame
    for i, timestamp in enumerate(timestamps):
        row = {
            'time': timestamp,
            'temperature_before': data[0]['data'][0]['values']['before'][i],
            'temperature_after': data[0]['data'][0]['values']['after'][i],
            'wind_speed_before': data[0]['data'][1]['values']['before'][i],
            'wind_speed_after': data[0]['data'][1]['values']['after'][i],
            'wind_direction_before': data[0]['data'][2]['values']['before'][i],
            'wind_direction_after': data[0]['data'][2]['values']['after'][i],
            'pressure_before': data[0]['data'][3]['values']['before'][i],
            'pressure_after': data[0]['data'][3]['values']['after'][i],
            'humidity_before': data[0]['data'][4]['values']['before'][i],
            'humidity_after': data[0]['data'][4]['values']['after'][i]
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        
    return df

#print (parsing(data))