from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.models.models import LoginRequest, UserRequest
from src.helper import hash_pass, access_token, verify_pass 
from src.schemas.schema import User
from datetime import datetime

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session

def signup(user_data: UserRequest, db: Session = Depends(get_db)):
    # 1. Check if user exists
    user_exists = db.query(User).filter(User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists"
        )
    
    # 2. Validation
    if len(user_data.hashed_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must be at least 8 characters"
        )
    
    # 3. Hash the password before saving
    # Assuming hash_pass is your utility function using passlib or bcrypt
    hashed_pw = hash_pass(user_data.hashed_password)

    # 4. Create and Save
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        firstname = user_data.firstname,
        lastname = user_data.lastname,
        created_at = datetime.now()
    )
    
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Return clean data (Don't return the hashed password back to the user!)
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email
        }
    }


# user login function 

def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    # 1. Find the user
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # 2. Check existence
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )
    
    # 3. Verify password
    matchpass = verify_pass(user_data.password, user.hashed_password)
    
    if not matchpass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # 4. Generate token - passing data as a dictionary
    token = access_token({
        "id": user.id,
        "email": user.email
    })

    # 5. Final Return
    return {
        "message": "Login successful",
        "user": {
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname
        },
        "token": token
    }
