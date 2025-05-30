import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from backend.main import app, get_db
from backend.database import Base
from backend.models import Car, Rental

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db")
def db_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Car Rental System"}


def test_create_car(client):
    """Test creating a new car."""
    car_data = {
        "make": "Audi",
        "model": "A4",
        "year": 2021,
        "daily_rate": 70.00,
    }
    response = client.post("/cars/", json=car_data)
    assert response.status_code == 200
    data = response.json()
    assert data["make"] == car_data["make"]
    assert data["model"] == car_data["model"]
    assert data["year"] == car_data["year"]
    assert data["daily_rate"] == car_data["daily_rate"]
    assert data["available"] is True
    assert "id" in data


def test_get_all_cars(client, db):
    """Test retrieving all cars."""
    car1 = Car(make="BMW", model="X5", year=2023, daily_rate=120.00)
    car2 = Car(make="Mercedes", model="C-Class", year=2022, daily_rate=90.00)
    db.add(car1)
    db.add(car2)
    db.commit()

    response = client.get("/cars/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(c["make"] == "BMW" for c in data)
    assert any(c["make"] == "Mercedes" for c in data)


def test_get_car(client, db):
    """Test retrieving a single car by ID."""
    car = Car(make="Volvo", model="XC90", year=2024, daily_rate=110.00)
    db.add(car)
    db.commit()
    db.refresh(car)

    response = client.get(f"/cars/{car.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == car.id
    assert data["make"] == car.make


def test_get_car_not_found(client):
    """Test retrieving a car that does not exist."""
    response = client.get("/cars/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Car not found"}


def test_rent_car_success(client, db):
    """Test successful car rental."""
    car = Car(make="Kia", model="Seltos", year=2023, daily_rate=60.00)
    db.add(car)
    db.commit()
    db.refresh(car)

    start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_date = (datetime.utcnow() + timedelta(days=3)).isoformat()

    rental_data = {
        "user_name": "John Doe",
        "start_date": start_date,
        "end_date": end_date,
    }
    response = client.post(f"/cars/{car.id}/rent", json=rental_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Rental successful"
    assert "rental_id" in response.json()

    # Verify rental in database
    db_rental = db.query(Rental).filter(Rental.id == response.json()["rental_id"]).first()
    assert db_rental is not None
    assert db_rental.car_id == car.id
    assert db_rental.user_name == "John Doe"


def test_rent_car_not_found(client):
    """Test renting a car that does not exist."""
    start_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_date = (datetime.utcnow() + timedelta(days=3)).isoformat()

    rental_data = {
        "user_name": "Jane Doe",
        "start_date": start_date,
        "end_date": end_date,
    }
    response = client.post("/cars/999/rent", json=rental_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Car not found"}


def test_rent_car_overlap(client, db):
    """Test renting a car with overlapping dates."""
    car = Car(make="Hyundai", model="Creta", year=2021, daily_rate=50.00)
    db.add(car)
    db.commit()
    db.refresh(car)

    # Existing rental
    existing_start = datetime.utcnow() + timedelta(days=5)
    existing_end = datetime.utcnow() + timedelta(days=10)
    existing_rental = Rental(
        car_id=car.id,
        user_name="Existing User",
        start_date=existing_start,
        end_date=existing_end,
    )
    db.add(existing_rental)
    db.commit()

    # Attempt to rent with overlapping dates (case 1: new rental starts within existing)
    overlap_start = (existing_start + timedelta(days=1)).isoformat()
    overlap_end = (existing_start + timedelta(days=3)).isoformat()
    rental_data_overlap = {
        "user_name": "Overlap User 1",
        "start_date": overlap_start,
        "end_date": overlap_end,
    }
    response = client.post(f"/cars/{car.id}/rent", json=rental_data_overlap)
    assert response.status_code == 400
    assert response.json() == {"detail": "Car already rented for the selected dates"}

    # Attempt to rent with overlapping dates (case 2: new rental ends within existing)
    overlap_start = (existing_end - timedelta(days=3)).isoformat()
    overlap_end = (existing_end - timedelta(days=1)).isoformat()
    rental_data_overlap = {
        "user_name": "Overlap User 2",
        "start_date": overlap_start,
        "end_date": overlap_end,
    }
    response = client.post(f"/cars/{car.id}/rent", json=rental_data_overlap)
    assert response.status_code == 400
    assert response.json() == {"detail": "Car already rented for the selected dates"}

    # Attempt to rent with overlapping dates (case 3: new rental encompasses existing)
    overlap_start = (existing_start - timedelta(days=2)).isoformat()
    overlap_end = (existing_end + timedelta(days=2)).isoformat()
    rental_data_overlap = {
        "user_name": "Overlap User 3",
        "start_date": overlap_start,
        "end_date": overlap_end,
    }
    response = client.post(f"/cars/{car.id}/rent", json=rental_data_overlap)
    assert response.status_code == 400
    assert response.json() == {"detail": "Car already rented for the selected dates"}

    # Attempt to rent with overlapping dates (case 4: existing rental encompasses new)
    overlap_start = (existing_start + timedelta(days=1)).isoformat()
    overlap_end = (existing_end - timedelta(days=1)).isoformat()
    rental_data_overlap = {
        "user_name": "Overlap User 4",
        "start_date": overlap_start,
        "end_date": overlap_end,
    }
    response = client.post(f"/cars/{car.id}/rent", json=rental_data_overlap)
    assert response.status_code == 400
    assert response.json() == {"detail": "Car already rented for the selected dates"}

def test_cancel_rental_success(client, db):
    """Test successful cancellation of a rental."""
    car = Car(make="Nissan", model="Altima", year=2020, daily_rate=45.00)
    db.add(car)
    db.commit()
    db.refresh(car)

    start_date = datetime.utcnow() + timedelta(days=1)
    end_date = datetime.utcnow() + timedelta(days=3)
    rental = Rental(
        car_id=car.id,
        user_name="Cancel User",
        start_date=start_date,
        end_date=end_date,
    )
    db.add(rental)
    db.commit()
    db.refresh(rental)

    response = client.delete(f"/rentals/{rental.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Rental canceled"}

    # Verify rental is deleted from database
    deleted_rental = db.query(Rental).filter(Rental.id == rental.id).first()
    assert deleted_rental is None


def test_cancel_rental_not_found(client):
    """Test cancelling a rental that does not exist."""
    response = client.delete("/rentals/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Rental not found"}