#models.py will define how pythong maps to the sql tables

#import SQLAlchemy tools
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

#defines python sensor class and maps it to sql table sensors
class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(Integer, primary_key=True, index=True) #primary key
    sensor_type = Column(String, nullable=False) #sensor_type (temperature, humidity for example)
    location = Column(String) #where the sensor is placed
    installed_at = Column(TIMESTAMP, server_default=func.now()) #timestamp when installed

    #defines a one-to-many relationship. A sensor can have multiple sensorData rows.
    data = relationship("SensorData", back_populates="sensor")

class SensorData(Base):
    #maps class sensordata to sql table sensor data
    __tablename__ = "sensor_data"

    data_id = Column(Integer, primary_key=True, index=True) #main key for each reading
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id", ondelete="CASCADE")) #links to the sensor this reading belongs to
    reading_value = Column(Numeric, nullable=False) #numeric measurement(temperature etc)
    reading_time = Column(TIMESTAMP, server_default=func.now()) #timestamp when the reading was captured (the time will default to the present)

    #defines the many-to-one side of the relationship : each SensorData belongs to exactly one sensor
    sensor = relationship("Sensor", back_populates="data")


