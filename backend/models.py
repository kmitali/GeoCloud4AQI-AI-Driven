from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class AQIData(Base):
    __tablename__ = "aqi_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    aqi_value = Column(Float, nullable=False)
    pollutant = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"AQIData(location={self.location}, aqi={self.aqi_value}, pollutant={self.pollutant})"
