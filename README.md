# 🚗 Car Rental System

This project implements a simple Car Rental System with a FastAPI backend and a ReactJS frontend. It allows users to view available cars, rent cars for a specified period, cancel rentals, and administrators to add new cars.

The project adheres to the requirements of the SD-Coding Challenge, focusing on API-driven communication, proper error handling, and a clear separation of concerns between the frontend and backend.

## ✨ Features

**Backend (FastAPI):**
* **Add a new car:** `POST /cars/`
* **Retrieve all available cars:** `GET /cars/`
* **Retrieve details of a specific car:** `GET /cars/{car_id}`
* **Rent a car:** `POST /cars/{car_id}/rent` (includes logic to prevent overlapping rentals)
* **Cancel an active rental:** `DELETE /rentals/{rental_id}`
* SQLite database for data persistence.
* OpenAPI (Swagger UI) documentation accessible at `/docs`.
* CORS enabled for frontend communication.
* Unit tests for API endpoints.

**Frontend (ReactJS):**
* Displays a list of all available cars.
* Provides a form to rent a car, specifying user name and rental dates.
* Provides an interface to cancel an existing rental by ID.
* Provides a form to add new cars (for simulation/admin purposes).
* Communicates with the backend exclusively via RESTful API calls using Axios.
* Simple, functional UI with tab-based navigation.

## 📂 Project Structure

D:.
├── car_rental.db          # SQLite database file (generated after first run)
├── .gitignore             # Files and folders to ignore in Git
├── README.md              # This documentation file
├── backend/
│   ├── init.py        # Makes 'backend' a Python package
│   ├── database.py        # SQLAlchemy database setup
│   ├── main.py            # FastAPI application, API endpoints
│   ├── models.py          # SQLAlchemy models (Car, Rental)
│   ├── schemas.py         # Pydantic schemas for data validation
│   ├── seed_data.py       # Script to populate initial car data
│   └── unit_test/         # Backend unit tests
│       └── u1.py
└── frontend-react/
├── public/            # Public assets (e.g., index.html)
├── src/
│   ├── App.js         # Main React component, all UI logic
│   ├── App.css        # Optional: Basic CSS for App.js
│   └── index.js       # Entry point for the React app
├── package.json       # Node.js project metadata and dependencies
└── README.md          # Default React app README


## 🛠️ Technologies Used

* **Backend:**
    * Python 3.13
    * FastAPI
    * SQLAlchemy (ORM)
    * SQLite (Database)
    * Uvicorn (ASGI server)
    * `pytest`, `httpx` (for unit tests)
* **Frontend:**
    * ReactJS
    * JavaScript
    * Node.js & npm (or yarn)
    * Axios (HTTP client)
* **Version Control:** Git & GitHub

## 🚀 Getting Started

Follow these steps to set up and run the Car Rental System on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.13:**
    * Download from [python.org](https://www.python.org/downloads/). Make sure to add Python to your PATH during installation.
2.  **Node.js & npm:** (npm comes with Node.js)
    * Download the LTS version from [nodejs.org](https://nodejs.org/).
3.  **Git:**
    * Download from [git-scm.com](https://git-scm.com/).
4.  **A Code Editor:** (e.g., VS Code, Sublime Text)

### 1. Clone the Repository (or ensure local files are set up)

If you're starting from scratch or re-cloning:

