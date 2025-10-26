from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, crud
from app.database import get_db




router = APIRouter(tags = ["users"])
# Can add user-related endpoints here in the future

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):


    # if email already exists
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # if username already exists
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # create new user
    new_user = crud.create_user(db, user)
    return new_user

#get all registered users
@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db:Session = Depends(get_db)):
    users  = db.query(crud.models.User).all()
    return  users


#get details of a specific user by ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(crud.models.User).filter(crud.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    return user

#fetching all users
@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(crud.models.User).all()
    return users

# getting details of a specific user by ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(crud.models.User).filter(crud.models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")
    return user