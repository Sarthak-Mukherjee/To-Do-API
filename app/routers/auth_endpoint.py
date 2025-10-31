# Login endpoint
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, utils,auth
from app.database import get_db
from app.crud import get_user_by_username


router = APIRouter(tags=["Authentication"])



# login endpoints

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #find user by username
    user = get_user_by_username(db, username = user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #verify password
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create JWT token
    access_token = auth.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"} # return the token and its type