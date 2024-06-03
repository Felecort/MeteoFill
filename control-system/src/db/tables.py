from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RawWeatherData(Base):
    __tablename__ = 'raw_weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    wind_speed_10m = Column(Float)
    wind_direction_10m = Column(Float)
    surface_pressure = Column(Float)
    timestamp = Column(DateTime)
    processed_data = relationship("ProcessedWeatherData", uselist=False, back_populates="raw_data")


class ProcessedWeatherData(Base):
    __tablename__ = 'processed_weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    raw_data_id = Column(Integer, ForeignKey('raw_weather_data.id'))
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    wind_speed_10m = Column(Float)
    wind_direction_10m = Column(Float)
    surface_pressure = Column(Float)
    timestamp = Column(DateTime)

    raw_data = relationship("RawWeatherData", back_populates="processed_data")


