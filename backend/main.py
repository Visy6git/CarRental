from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models
from .schemas import CarCreate, CarOut, RentalCreate
from .models import Car, Rental
from sqlalchemy import and_, or_
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Your React app's address
    "http://127.0.0.1:3000", # Another common localhost address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

# ... (rest of your existing FastAPI code)

# Your existing get_db function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cars/", response_model=CarOut)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = models.Car(
        make=car.make,
        model=car.model,
        year=car.year,
        daily_rate=car.daily_rate
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

from typing import List

@app.get("/cars/", response_model=List[CarOut])
def get_all_cars(db: Session = Depends(get_db)):
    return db.query(models.Car).all()

@app.get("/cars/{car_id}", response_model=CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.delete("/rentals/{rental_id}")
def cancel_rental(rental_id: int, db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    db.delete(rental)
    db.commit()
    return {"message": "Rental canceled"}


@app.get("/")
def read_root():
    return {"message": "Welcome to Car Rental System"}

@app.post("/cars/{car_id}/rent")
def rent_car(car_id: int, rental: RentalCreate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Check for date overlap
    overlapping_rentals = db.query(Rental).filter(
        Rental.car_id == car_id,
        or_(
            and_(
                Rental.start_date <= rental.start_date,
                Rental.end_date >= rental.start_date
            ),
            and_(
                Rental.start_date <= rental.end_date,
                Rental.end_date >= rental.end_date
            ),
            and_(
                Rental.start_date >= rental.start_date,
                Rental.end_date <= rental.end_date
            )
        )
    ).all()

    if overlapping_rentals:
        raise HTTPException(status_code=400, detail="Car already rented for the selected dates")

    # Create rental
    new_rental = Rental(
        car_id=car_id,
        user_name=rental.user_name,
        start_date=rental.start_date,
        end_date=rental.end_date
    )

    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    return {"message": "Rental successful", "rental_id": new_rental.id}