
from fastapi import Depends
from sqlalchemy.orm import session
from config.db import get_db
from models.models import UserReqwest
from fastapi import HTTPException

from schemas.schema import User

def signup(user_data : UserReqwest , db : session = Depends(get_db) ):
    try :
        userExixt = db.query(User).filter(User.email == user_data.email).first()
        if userExixt :
            raise HTTPException(status_code=401,detail= f"user already exixt")
        
        password = list(user_data.hashed_password)
        print(password)
        # password validation 
        if password > 8:
            raise HTTPException(status_code=405 , detail= f"password must be 8 carecter or higher")
        
        # hash the password 

    except Exception as e :
        raise HTTPException(status_code= 500, detail= f"error is this {str(e)}")

