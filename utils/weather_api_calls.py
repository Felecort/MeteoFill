import openmeteo_requests

import requests_cache
from retry_requests import retry
import pandas as pd

from typing import Dict



def get_weather(params: Dict=None) -> pd.DataFrame:
    """
    Return DataFrame that contains weather parameters for every day or hour.
    For more information see https://open-meteo.com/en/docs

    Params example:
    --------
        >>> params = {
        >>>     "latitude": -74.0411, # North Pole
        >>>     "longitude": 51.4071, # North Pole
        >>>     "start_date": "2021-07-01",
        >>>     "end_date": "2021-07-10",
        >>>     "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m", "wind_direction_10m"]
        >>>     "timeformat": "unixtime"
        >>> }

    """
    if params is None:
        params = {
            "latitude": -74.0411, # North Pole
            "longitude": 51.4071, # North Pole
            "start_date": "2021-07-01",
            "end_date": "2021-07-10",
            "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m", "wind_direction_10m"], # Our params
            "timeformat": "unixtime"
        }
    url = "https://archive-api.open-meteo.com/v1/archive" # ----- ARCHIVE DATA


    """ Setup the Open-Meteo API client with cache and retry on error"""
    cache_session = requests_cache.CachedSession('.cache', backend="filesystem", serializer="json", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=1)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    if "hourly" in params.keys():
        freq_type = "hourly"
        result = response.Hourly()
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
    hourly_dataframe = pd.DataFrame(data=data)

    return hourly_dataframe


if __name__ == "__main__":
    print(get_weather().head())