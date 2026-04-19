

from dotenv import load_dotenv
from src.controller.ai_function import ask_question
from src.models.models  import QuestionResponse
from fastapi import APIRouter, FastAPI

router = APIRouter(
    prefix="/AI",
    tags=["Ai side"]
)

@router.get("/")
def home():
    return {"message": "API is working"}


load_dotenv()

@router.post("/question", response_model=QuestionResponse)
def quistion(quistion: str):
    return ask_question(quistion)