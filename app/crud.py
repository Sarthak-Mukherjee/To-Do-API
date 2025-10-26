from app import models, schemas
from sqlalchemy.orm import Session
from app.utils import get_password_hash


#----------USER CRUD-----------
# Get a new user
def get_user_by_email(db:Session, email: str):
    return db.query(models.User).filter(models.User.email ==email).first()


def get_user_by_username(db:Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):

    print("password before hashing: ", user.password, type(user.password)) 
    hashed_password = get_password_hash(str(user.password)) # Hash the password
    db_user = models.User(username=user.username,
                           email=user.email,
                            hashed_password= hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





#-------------TODO CRUD--------------
# Retrieve all to-do items
def get_todos(db: Session, user_id: int ):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()

# Create a new to-do item
def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(title = todo.title, completed = todo.completed, user_id = user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# update an existing to-do item
def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoUpdate, user_id:int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id).first()
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
def delete_todo(db:Session, todo_id: int, user_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id).first()
    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return todo