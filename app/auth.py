# handles JWT token generation and verification

from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, models
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db

load_dotenv()

# load secre and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)  # Token expiry time in minutes


# This defines the token URL that FASTAPI uses for login
# Must match /auth/login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")




# Function to create a JWT token
def create_access_token(data:dict):
    # creates JWT token that includes user info (like id or username)
    to_encode = data.copy() # copy input data to avoid modifying original

    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)) # set token expiry time

    to_encode.update({"exp": expire}) # add expiry time to token payload

    # encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# function to verify a JWT token
def verify_access_token(token: str, credentials_exception):

    # decodes and validates JWT token; raises an error if invalid/expired
    try:
        # decode the token to extract payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")


        if user_id is None:
            raise credentials_exception # raise error if user_id not found in token
        token_data = schemas.TokenData(id=user_id) # Wrap in TokenData Pydantic schema

    except JWTError:
        raise credentials_exception  # raise error if token is invalid or expired
    
    return token_data  # return the extracted token data


# Dependency to get the current user based on the JWT token
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1: Validate and decode token
    token_data = verify_access_token(token, credentials_exception)

    # 2: Find user in DB based on token's user id
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    
    return user