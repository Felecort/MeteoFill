from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from src.db.tables import *


class DatabaseManager:
    def __init__(
            self,
            username: str,
            password: str,
            dbname: str,
            host: str = 'postgres',
            port: int = 5432
    ):
        self._DATABASE_URI = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
        self._engine = create_engine(self._DATABASE_URI)
        if not database_exists(self._engine.url):
            create_database(self._engine.url)
        # Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def store_weather_data(self, weather_data_before: dict, weather_data_after: dict):
        with Session(self._engine) as session:
            raw_data = self.__store_raw_data(session, **weather_data_before)
            session.flush()
            self.__store_processed_data(session, raw_data, **weather_data_after)
            session.commit()

    def __store_raw_data(
            self,
            session,
            temperature_2m,
            relative_humidity_2m,
            wind_speed_10m,
            wind_direction_10m,
            surface_pressure,
            timestamp
    ):
        raw_data = RawWeatherData(
            temperature_2m=temperature_2m,
            relative_humidity_2m=relative_humidity_2m,
            wind_speed_10m=wind_speed_10m,
            wind_direction_10m=wind_direction_10m,
            surface_pressure=surface_pressure,
            timestamp=timestamp
        )
        session.add(raw_data)
        return raw_data

    def __store_processed_data(
            self,
            session,
            raw_data,
            temperature_2m,
            relative_humidity_2m,
            wind_speed_10m,
            wind_direction_10m,
            surface_pressure,
            timestamp
    ):
        processed_data = ProcessedWeatherData(
            raw_data_id=raw_data.id,
            temperature_2m=temperature_2m,
            relative_humidity_2m=relative_humidity_2m,
            wind_speed_10m=wind_speed_10m,
            wind_direction_10m=wind_direction_10m,
            surface_pressure=surface_pressure,
            timestamp=timestamp
        )
        session.add(processed_data)
