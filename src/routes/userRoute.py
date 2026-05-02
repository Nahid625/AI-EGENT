from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.auth import login, signup
from src.models.models import LoginRequest, SignupResponse, UserRequest # Import your request model
from src.config.db import get_db # Import your DB session logic

router = APIRouter(
    prefix="/user", # Lowercase is standard for URLs
    tags=["User side"]
)

@router.post("/signup", response_model=SignupResponse)
def sign_up_route_function(user_data: UserRequest, db: Session = Depends(get_db)):
    # You need to pass the user_data AND the db session to your controller
    return signup(user_data=user_data, db=db)


@router.post("/login",response_model=SignupResponse)
def login_Router_Function(user_data : LoginRequest ,db : Session = Depends(get_db)):
    return login(user_data,db)