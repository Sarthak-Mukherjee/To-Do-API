from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user


# Create a router for todo endpoints
router = APIRouter(tags = ["todos"])

# list all todos
@router.get("/", response_model= list[schemas.TodoOut])
def list_todos(db:Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return todos

# create a new todo
@router.post("/", response_model= schemas.TodoOut)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    new_todo = models.Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# update an existing todo
@router.put("/{todo_id}", response_model= schemas.TodoOut)
def update_todo(
    todo_id: int,
    todo_data: schemas.TodoUpdate,
    db: Session=Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    todo  = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this todo")
    
    for key, value in todo_data.dict(exclude_unset=True).items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


# delete a todo
@router.delete("/{todo_id}", response_model= schemas.TodoOut)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    
    if(todo.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    
    db.delete(todo)
    db.commit()
    return todo