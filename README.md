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
2. Set Up the Backend
Navigate to the backend directory:

Bash

cd D:\SANJANA\car_rental\backend
a. Create a Virtual Environment (Recommended)
It's good practice to use a virtual environment to manage project dependencies.

Bash

python -m venv venv
b. Activate the Virtual Environment
On Windows (Command Prompt):
Bash

venv\Scripts\activate.bat
On Windows (PowerShell):
PowerShell

.\venv\Scripts\Activate.ps1
On macOS/Linux:
Bash

source venv/bin/activate
Your terminal prompt should now show (venv) indicating the virtual environment is active.
c. Install Backend Dependencies
Create a requirements.txt file in your backend directory.

D:\SANJANA\car_rental\backend\requirements.txt

fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
pydantic==2.7.1
httpx==0.27.0
pytest==8.2.1
(Note: I've provided exact versions used during development to ensure compatibility. If you prefer, you can use fastapi, uvicorn[standard], etc., without versions to get the latest, but this might introduce breaking changes.)

Now, install them:

Bash

pip install -r requirements.txt
d. Initialize the Database and Seed Data
Your FastAPI application automatically creates the car_rental.db file and the necessary tables on its first run or when Base.metadata.create_all() is called. To also populate some initial car data:

Bash

python seed_data.py
This will create car_rental.db in your project root and add some sample cars.

e. Start the FastAPI Backend
While still in the backend directory with the virtual environment active:

Bash

uvicorn main:app --reload
The --reload flag enables live reloading, so the server restarts automatically when you make code changes.
You should see output indicating the server is running on http://127.0.0.1:8000. Keep this terminal window open.

Verify Backend:

Open your browser and navigate to http://127.0.0.1:8000/docs. You should see the Swagger UI documentation for your API.
Go to http://127.0.0.1:8000/cars/. You should see a JSON array of the cars you seeded.
3. Set Up the Frontend
Open a NEW terminal window. Leave the backend terminal running.

Navigate to the frontend-react directory:

Bash

cd D:\SANJANA\car_rental\frontend-react
a. Install Frontend Dependencies
Bash

npm install
This command reads package.json and installs all necessary Node.js packages (like React, ReactDOM, Axios).

b. Start the React Frontend
Bash

npm start
This will start the React development server. It usually opens a new tab in your web browser at http://localhost:3000. Keep this terminal window open.

🧪 Running Unit Tests (Backend)
To run the backend unit tests, open a terminal, navigate to the backend directory, activate your virtual environment, and then run pytest:

Bash

cd D:\SANJANA\car_rental\backend
venv\Scripts\activate.bat   # Or your OS equivalent
pytest unit_test/u1.py
You should see test results indicating passed tests.

🤝 Contribution
Feel free to fork this repository, make improvements, and submit pull requests.



