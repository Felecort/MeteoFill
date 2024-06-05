import json
from datetime import datetime
import pandas as pd

# Функция для расчета временных меток
def calculate_timestamps(start_timestamp: datetime, end_timestamp: datetime, delay: int) -> pd.DatetimeIndex:
    """
    Вычисляет временные метки между начальной и конечной с заданной задержкой.

    Args:
        start_timestamp (datetime): Начальная временная метка.
        end_timestamp (datetime): Конечная временная метка.
        delay (int): Задержка между временными метками в секундах.

    Returns:
        pd.DatetimeIndex: Список временных меток.
    """
    timestamps = pd.date_range(
        start=start_timestamp,
        end=end_timestamp,
        freq=pd.Timedelta(int(delay * 1e9)),  # from nanoseconds to seconds
        inclusive="both"
    )
    return timestamps

# Функция для парсинга данных из словаря в DataFrame
def parsing(data: dict) -> pd.DataFrame:
    """
    Парсит данные из словаря в DataFrame.

    Args:
        data (dict): Данные в формате словаря.

    Returns:
        pd.DataFrame: DataFrame с парсингованными данными.
    """
    delay = data["delay"]
    
    # Попытка парсинга временных меток с миллисекундами и без
    try:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M:%S.%f000")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M:%S.%f000")
    except ValueError:
        start_timestamp = datetime.strptime(data["timestamps"]["start"], "%Y-%m-%dT%H:%M")
        end_timestamp = datetime.strptime(data["timestamps"]["end"], "%Y-%m-%dT%H:%M")
    
    # Вычисляем временные метки
    timestamps = calculate_timestamps(start_timestamp, end_timestamp, delay)

    # Извлекаем данные до и после восстановления
    data_before = {item["id"]+"_before": item["values"]["before"] for item in data["data"]}
    data_after = {item["id"]+"_after": item["values"]["after"] for item in data["data"]}
    data_time = {"time": timestamps}

    # Создаем DataFrame из извлеченных данных
    df_before = pd.DataFrame(data_before)
    df_after = pd.DataFrame(data_after)
    df_time = pd.DataFrame(data_time)

    # Объединяем все DataFrame
    df = pd.concat([df_time, df_before, df_after], axis=1)
    return df

# Функция для добавления новых данных в JSON
def add_data(new_data: dict, max_rows=100):
    """
    Добавляет новые данные в response.json.

    Args:
        new_data (dict): Новые данные в формате словаря.
        max_rows (int): Максимальное количество строк для сохранения.
    """
    df = parsing(new_data)
    
    # Ограничиваем количество строк в DataFrame
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]

    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M')

    # Формируем данные для сохранения
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

    # Сохраняем данные в JSON файл
    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

# Функция для обновления данных в JSON
def update_data(new_data: dict, max_rows=100):
    """
    Обновляет данные в response.json.

    Args:
        new_data (dict): Новые данные в формате словаря.
        max_rows (int): Максимальное количество строк для сохранения.
    """
    # Загружаем предыдущие данные из JSON
    with open("response.json", "r") as f:
        previous_data = json.load(f)
        previous_data_df = parsing(previous_data)

    # Парсинг новых данных
    new_data_df = parsing(new_data)

    # Объединение предыдущих и новых данных
    df = pd.concat([previous_data_df, new_data_df])
    df.reset_index(drop=True, inplace=True)
    
    # Ограничиваем количество строк в DataFrame
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]

    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M')

    # Формируем данные для сохранения
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

    # Сохраняем данные в JSON файл
    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)
