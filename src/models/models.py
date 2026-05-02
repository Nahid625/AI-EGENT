from pydantic import BaseModel 
from datetime import datetime


class QuestionResponse(BaseModel):
    yourQuistion : str
    response: str
    
class QuestionRequest(BaseModel):
    question: str

class UserReqwest(BaseModel):
    firstname : str
    lastname: str
    email : str 
    hashed_password : str
    created_at : datetime

class SignupResponse(BaseModel):
     message : str
     user : dict
     