##Simple To-Do API with FastAPI
A lightweight, full-featured To-Do application backend built with FastAPI, SQLAlchemy, and PostgreSQL. Designed for easy integration with any frontend framework or static HTML/JS.

##Features

✅ Create, Read, Update, Delete (CRUD) operations for To-Do items

✅ RESTful API endpoints

✅ PostgreSQL database integration

✅ Pydantic schemas for validation and response formatting

✅ Optionally serve static frontend or connect external frontend

✅ Fully extensible and ready for production

##Project Structure
todo_app/
├── venv/                  # Python virtual environment
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic request & response schemas
│   ├── crud.py            # Database operations
│   ├── database.py        # DB connection setup
│   └── routers/
│       ├── __init__.py
│       └── todos.py       # API routes
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

##Installation

Clone the repository

git clone <repository-url>
cd todo_app


Create and activate virtual environment

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Set up environment variables

Create a .env file in the root folder:

DATABASE_URL=postgresql://username:password@localhost:5432/todo_db


Create the PostgreSQL database

Ensure PostgreSQL is running and the database specified exists. Tables will be auto-created on app startup.

##Running the Application
uvicorn app.main:app --reload


Backend URL: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

ReDoc docs: http://127.0.0.1:8000/redoc

📦 API Endpoints
Method	Endpoint	Description
GET	/todos/	List all todos
POST	/todos/	Create a new todo
PUT	/todos/{id}	Update an existing todo
DELETE	/todos/{id}	Delete a todo

Example POST JSON body:

{
    "title": "Buy groceries",
    "completed": false
}

##Frontend Integration
Option 1: Serve static files from FastAPI

Place index.html, app.js, and style.css in a static/ folder.

Mount static files in main.py.

Option 2: Separate frontend

Create a frontend project with React, Vue, Angular, or plain HTML/JS.

Call backend APIs via HTTP (e.g., http://127.0.0.1:8000/todos/).

Allows fully decoupled architecture and independent deployment.

##Next Steps / Enhancements

Add JWT-based user authentication

Dockerize backend and PostgreSQL

Add automated tests

Build a modern React/Vue SPA consuming the API

