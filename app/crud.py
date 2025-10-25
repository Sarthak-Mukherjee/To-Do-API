from app import models, schemas
from sqlalchemy.orm import Session

def get_todos(db: Session):
    return db.query(models.Todo).all()


# Create a new to-do item
def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title = todo.title, completed = todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# update an existing to-do item
def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoUpdate):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    
    db.commit()
    db.refresh(todo)
    return todo


# delete a to-do item
def delete_todo(db:Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return todo