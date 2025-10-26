# import BaseModel from pydantic for schema definitions
from pydantic import BaseModel, EmailStr

#-----------TODO SCHEMAS-----------
# Base schema for common fields
class TodoBase(BaseModel):
    title: str
    completed: bool = False


# Create Schema
class TodoCreate(TodoBase):
    pass

# Update Schema
class TodoUpdate(TodoBase):
    title: str | None = None # Optional field
    completed: bool | None = None

# Delete Schema
class TodoDelete(TodoBase):
    id : int # ID of the todo item to delete

# Output Schema
class TodoOut(TodoBase):
    id : int # ID of the todo item
    user_id : int # ID of the user who owns the todo item

    class Config:
        orm_mode = True # Enable ORM mode for compatibility with SQLAlchemy models


#-----------USER SCHEMAS-----------
# Base schema for common fields
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Create User Schema
class UserCreate(UserBase):
    password : str #

# Create userOutput Schema
class UserOut(UserBase):
    id: int # ID of the user

    class Config:
        orm_mode = True # Enable ORM mode for compatibility with SQLAlchemy models