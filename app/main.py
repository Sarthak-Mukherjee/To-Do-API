from fastapi import FastAPI

from app.routers import todos
from app.database import Base, engine


Base.metadata.create_all(bind=engine) # Create database tables

app = FastAPI(title="Simple To-Do API")
app.include_router(todos.router, prefix="/todos")  # Include the todos router



@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple To-Do API"}