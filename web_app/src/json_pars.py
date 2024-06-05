import json
from datetime import datetime
import pandas as pd

# Описание датчиков для обработки
metrics = [
    {"name": "Температура", "id": "temperature_2m"},
    {"name": "Относительная влажность", "id": "relative_humidity_2m"},
    {"name": "Атмосферное давление", "id": "surface_pressure"},
    {"name": "Скорость ветра", "id": "wind_speed_10m"},
    {"name": "Направление ветра", "id": "wind_direction_10m"}
]

# Функция для вычисления временных меток
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
        freq=pd.Timedelta(int(delay * 1e9)),
        inclusive="both"
    )
    return timestamps

# Функция для парсинга данных из словаря в DataFrame
def parsing_rabbit(data: dict) -> pd.DataFrame:
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

    df = parsing(data, timestamps)

    return df

# Функция для парсинга данных из словаря в DataFrame
def parsing_data(data: dict) -> pd.DataFrame:
    """
    Парсит данные из словаря в DataFrame.

    Args:
        data (dict): Данные в формате словаря.

    Returns:
        pd.DataFrame: DataFrame с парсингованными данными.
    """
    # Извлекаем временные метки
    timestamps = pd.to_datetime(data["timestamps"])
    
    df = parsing(data, timestamps)

    return df

# Функция для извлечения и объединения данных
def parsing(data: dict, timestamps: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Извлекает данные до и после восстановления и объединяет их в DataFrame.

    Args:
        data (dict): Данные в формате словаря.
        timestamps (pd.DatetimeIndex): Временные метки.

    Returns:
        pd.DataFrame: Объединенный DataFrame.
    """
    data_before = {item["id"] + "_before": item["values"]["before"] for item in data["data"]}
    data_after = {item["id"] + "_after": item["values"]["after"] for item in data["data"]}
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
    # Парсинг данных
    df = parsing_rabbit(new_data)
    
    # Ограничение количества строк
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]
    
    save_json(df)

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
        previous_data_df = parsing_data(previous_data)

    # Парсинг новых данных
    new_data_df = parsing_rabbit(new_data)

    # Объединение предыдущих и новых данных
    df = pd.concat([previous_data_df, new_data_df])
    df = df.sort_values(by='time')
    df.drop_duplicates(subset=['time'], keep='last', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Ограничиваем количество строк в DataFrame
    if len(df) >= max_rows:
        df = df.iloc[:max_rows]

    save_json(df)

# Функция для сохранения данных в JSON
def save_json(df: pd.DataFrame):
    """
    Сохраняет DataFrame в JSON файл.

    Args:
        df (pd.DataFrame): DataFrame для сохранения.
    """
    # Форматирование времени
    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M')
    
    # Создание структуры данных для сохранения
    data_to_save = {
        "timestamps": df['time'].tolist(),
        "data": []
    }
    
    # Заполнение данных о погоде
    for metric in metrics:
        metric_data = {
            "name": metric["name"],
            "id": metric["id"],
            "values": {
                "before": df[f'{metric["id"]}_before'].tolist(),
                "after": df[f'{metric["id"]}_after'].tolist()
            }
        }
        data_to_save["data"].append(metric_data)

    # Сохраняем данные в JSON файл
    with open("response.json", "w") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)
