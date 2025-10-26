from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

# Create a router for todo endpoints
router = APIRouter(tags = ["todos"])

# list all todos
@router.get("/", response_model= list[schemas.TodoOut])
def list_todos(db:Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return todos

# create a new todo
@router.post("/", response_model= schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate,db: Session = Depends(get_db)):
    new_todo = crud.create_todo(db, todo)
    return new_todo

# update an existing todo
@router.put("/{todo_id}", response_model= schemas.TodoOut)
def update_todo(todo_id: int, todo_data: schemas.TodoUpdate, db: Session= Depends(get_db)):
    updated_todo = crud.update_todo(db, todo_id, todo_data)
    if not updated_todo:
        raise HTTPException(status_code = 404, detail = "Todo Not found")
    return updated_todo


# delete a todo
@router.delete("/{todo_id}", response_model= schemas.TodoOut)
def delete_todo(todo_id: int, db: Session= Depends(get_db)):
    deleted_todo = crud.delete_todo(db, todo_id)
    if not deleted_todo:
        raise HTTPException(status_code = 404, detail = "Todo Not found")
    return deleted_todo