from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.auth import signup
from src.models.models import SignupResponse, UserReqwest # Import your request model
from src.config.db import get_db # Import your DB session logic

router = APIRouter(
    prefix="/user", # Lowercase is standard for URLs
    tags=["User side"]
)

@router.post("/signup", response_model=SignupResponse)
def sign_up_route_function(user_data: UserReqwest, db: Session = Depends(get_db)):
    # You need to pass the user_data AND the db session to your controller
    return signup(user_data=user_data, db=db)