from database import SessionLocal
from models import Car

# Sample cars
cars = [
    Car(make="Toyota", model="Corolla", year=2020, daily_rate=45.00),
    Car(make="Honda", model="Civic", year=2022, daily_rate=55.00),
    Car(make="Ford", model="Focus", year=2019, daily_rate=40.00),
    Car(make="Tesla", model="Model 3", year=2023, daily_rate=85.00),
]

db = SessionLocal()

for car in cars:
    db.add(car)

db.commit()
db.close()

print("Seeded car data successfully.")
