from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from fastapi import Depends, HTTPException

from dotenv import load_dotenv
import os

import jwt
from sqlalchemy.orm import Session

from src.config.db import get_db
from src.schemas.schema import User 
load_dotenv()


def hash_pass(plain_password: str):
    # You MUST encode to bytes first!
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_pass(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Use a fallback if the .env isn't found
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def access_token(data :dict):
    try:
      to_encode = data.copy()
     # setExpiry 
      expire = datetime.utcnow() + timedelta(minutes=60)
      to_encode.update({"exp":expire})

      encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
      return encoded_jwt
    

    except TypeError as e:
        # DEBUG: This happens if SECRET_KEY is None or 'data' isn't a dict
     raise HTTPException(status_code=500, detail=f"JWT Config Error: Check your .env file! ({str(e)})")
    
    except ValueError as e:
        # DEBUG: This happens if the Algorithm name is wrong
     raise HTTPException(status_code=500, detail=f"JWT Value Error: {str(e)}")
        
    except Exception as e:
        # DEBUG: The ultimate fallback
     raise HTTPException(status_code=500, detail=f"Special JWT Debug: {str(e)}")



def decodedToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Pulling out multiple things
        user_id = payload.get("user_id")
        user_email = payload.get("email")
        
        print(f"DEBUG: Found User ID {user_id} with Email {user_email}")
        
        return payload # Returns the whole dict with everything inside
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token is trash, bro!")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decodedToken(token)          # ← your existing function
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user