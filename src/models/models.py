from pydantic import BaseModel 

class QuestionResponse(BaseModel):
    yourQuistion : str
    response: str
    
class QuestionRequest(BaseModel):
    question: str 
