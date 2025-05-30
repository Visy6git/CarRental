from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from .database import Base
from datetime import datetime

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    daily_rate = Column(Float, nullable=False)
    available = Column(Boolean, default=True)

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    user_name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    rental_date = Column(DateTime, default=datetime.utcnow)
