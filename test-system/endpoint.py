import math

import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Any
from datetime import date
import logging
import json
from sklearn.metrics import mean_squared_error
from math import sqrt
import time
from copy import deepcopy

app = FastAPI()

logging.basicConfig(level=logging.INFO)

def create_nan(data, prob=0.5):
    mask = np.random.binomial(n=1, p=prob, size=data.shape).astype(np.float32)
    mask[mask == 0] = np.nan
    return mask * data.select_dtypes(include='number')



class WeatherService:
    def __init__(self, cache_expire_after=-1, retries=5, backoff_factor=0.2):
        # Setup the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=cache_expire_after)
        self.retry_session = retry(self.cache_session, retries=retries, backoff_factor=backoff_factor)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.original_data = None 

    def get_weather_data(self, lat: float, lon: float, start_date: str, end_date: str):
        logging.info(f"Requesting weather data for lat={lat}, lon={lon}, start_date={start_date}, end_date={end_date}")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m", "wind_direction_10m"]
        }
        responses = self.openmeteo.weather_api(url, params=params)
        response = responses[0]

        if "hourly" in params.keys():
            result = response.Hourly()
            freq_type = "hourly"
        elif "daily" in params.keys():
            result = response.Daily()
            freq_type = "daily"
        else:
            raise KeyError("Absent  or unknown frequency type. Supporn only ['hourly', 'daily]. https://open-meteo.com/en/docs")

        # Create timestamp column
        data = {"date": pd.date_range(
            start = pd.to_datetime(result.Time(), unit = "s", utc = True),
            end = pd.to_datetime(result.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = result.Interval()),
            inclusive = "left"
        )}

        # Parse result
        for i, param in enumerate(params[freq_type]):
            data[param] = result.Variables(i).ValuesAsNumpy()

        # conver to DataFrame
        df = pd.DataFrame(data=data)
        df = df.set_index("date", drop=True)
        self.original_data = df.copy()
        return df

    def calculate_rmse(self, filled_df: pd.DataFrame):
        if self.original_data is None:
            raise ValueError("No original data available for RMSE calculation")
        
        numeric_columns = self.original_data.select_dtypes(include=np.number).columns
        rmse_values = [np.sqrt(mean_squared_error(self.original_data[column], filled_df[column])) for column in numeric_columns]
        return pd.Series(rmse_values, index=numeric_columns)
    

class CSVProcessor:
    def __init__(self, csv_file_path=r'C:\Users\rusik\OneDrive\Опять Работа\Магамед\1 курс 2 сем\Проектировании ИИ\Курсовки\MeteoFill\test-system\data\weather_data.csv', skiprows=3, batch_size=50, prob=0.5):
        self.skiprows = skiprows
        self.batch_size = batch_size
        self.prob = prob
        self.csv_file_path = csv_file_path
        self.df_data = pd.read_csv(csv_file_path, skiprows=self.skiprows, index_col='time')
        self.df_2 = deepcopy(self.df_data)

    def process_csv_in_batches(self):
        try:
            logging.info("Processing CSV file in batches")
            # batch_with_nan = create_nan(batch, prob=self.prob)
            # # json_data = batch_with_nan.to_json(orient='split', date_format='iso')
            # temp = json.dumps({"message": "Received batch", "data": list(batch_with_nan)})
            # print(temp)
            # yield temp
            # time.sleep(2)
            data_with_nan = create_nan(self.df_data, prob=self.prob)
            data_without_nan = self.df_data
            batches_with_nan = np.array_split(data_with_nan, math.ceil(len(self.df_data) / self.batch_size))
            batches_without_nan = np.array_split(data_without_nan, math.ceil(len(self.df_data) / self.batch_size))
            return batches_with_nan, batches_without_nan
        except Exception as e:
            logging.error(f"Error processing CSV file in batches: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def calculate_rmse(self, filled_df: pd.DataFrame, start: int):
        if self.df_2 is None:
            raise ValueError("No original data available for RMSE calculation")
        logging.info("Calculating RMSE")
        # for temp in pd.read_csv(self.csv_file_path, skiprows=self.skiprows, index_col='time', chunksize=self.batch_size):
            # temp = self.df_data.iloc[i*self.batch_size:(i+1)*self.batch_size]
        temp1 = self.df_2.iloc[start:start + self.batch_size]
            # print(start)
            # print(temp)
        numeric_columns = temp1.select_dtypes(include=np.number).columns
        rmse_values = [np.sqrt(mean_squared_error(temp1[column], filled_df[column])) for column in numeric_columns]

        time.sleep(2)
        logging.info("RMSE calculation completed")
        return pd.Series(rmse_values, index=numeric_columns)
    

# # WeatherRequest: Это модель Pydantic, представляющая структуру запроса,
# # ожидаемого конечной точкой /weather-data. Она включает широту, долготу
# # начальную дату, конечную дату и необязательную вероятность.
# class WeatherRequest(BaseModel):
#     latitude: float
#     longitude: float
#     start_date: date
#     end_date: date
#     prob: Optional[float] = 0.5
#
# # Модель для принятия заполненных данных
# class FilledWeatherData(BaseModel):
#     data: dict
#     service_class: str
#     start: int
#
# # Инициализируем объект WeatherService
# weather_service = WeatherService()
# #csv_processor = CSVProcessor()
# # /weather-data: ожидает объект WeatherRequest
# # в теле запроса. Она извлекает данные о погоде на основе предоставленных параметров,
# # добавляет к ним значения NaN, преобразует их в JSON и возвращает в ответе.
# # Если при обработке возникает ошибка, он вызывает HTTPException с кодом состояния 500.
# @app.post("/weather-data")
# async def weather_data(request: WeatherRequest):
#     try:
#         logging.info(f"Received request: {request}")
#         weather_df = weather_service.get_weather_data(request.latitude, request.longitude, str(request.start_date), str(request.end_date))
#         weather_df_with_nan = create_nan(weather_df, prob=request.prob)
#         json_data = weather_df_with_nan.to_json(orient='split', date_format='iso')
#         logging.info(f"Processed data successfully")
#         return json.loads(json_data)
#
#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


class Weather(BaseModel):
    columns: list[str]
    index: list[int]
    data: list[list]

@app.post("/rmse")
async def calculate_rmse(request: Weather):
    # try:
    global batch_index
    global true_batches
    logging.info("RMSE calculation started")
    # json_data = json.loads(request)
    # logging.info(json_data)

    # filled_batch = pd.read_json(json.dumps(request.body))
    filled_batch = pd.read_json(request.json(), orient='split')
    true_batch = true_batches[batch_index-1]
    numeric_columns = true_batch.select_dtypes(include=np.number).columns
    rmse_values = [np.sqrt(mean_squared_error(true_batch[column], filled_batch[column])) for column in numeric_columns]

    print(rmse_values)

    logging.info(rmse_values)
    logging.info("RMSE calculation completed")
    return pd.Series(rmse_values, index=numeric_columns)
    # except:
    #     logging.info('Миша, все хуйня. Давай по-новой.')

# @app.post("/rmsse")
# async def calculate_rmse(request: FilledWeatherData):
#     try:
#         logging.info(f"Received filled data for RMSE calculation for class {request.service_class}")
#         filled_df = pd.read_json(json.dumps(request.data), orient='split')
#
#         if request.service_class == "WeatherService":
#             rmse_values = weather_service.calculate_rmse(filled_df)
#         elif request.service_class == "CSVProcessor":
#             csv_processor = CSVProcessor()
#             rmse_values = csv_processor.calculate_rmse(filled_df, start=request.start)
#         else:
#             raise HTTPException(status_code=400, detail="Unknown service class")
#
#         print(rmse_values)
#     except Exception as e:
#         logging.error(f"Error processing filled data: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


csv_processor2 = CSVProcessor()
batches, true_batches = csv_processor2.process_csv_in_batches()
batch_index = 0

@app.get("/process-csv")
async def process_csv():
    try:
        global batches
        global batch_index
        # response = StreamingResponse(
        #     batch,
        #     media_type="application/json"
        # )
        if batch_index < len(batches):
            batch = batches[batch_index]
            batch_index += 1
            # return json.dumps(batch.to_json(orient='split'))
            # return json.dumps(batch.to_json(orient='split'))
            return JSONResponse(content=batch.to_json())
        else:
            return {"message": "Все батчи были отправлены"}
    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8092)
