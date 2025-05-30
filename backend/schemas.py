from pydantic import BaseModel
from datetime import datetime

class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    daily_rate: float

class CarOut(BaseModel):
    id: int
    make: str
    model: str
    year: int
    daily_rate: float
    available: bool

    class Config:
        from_attributes = True

class RentalCreate(BaseModel):
    user_name: str
    start_date: datetime
    end_date: datetime
