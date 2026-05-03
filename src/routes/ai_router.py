

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from config.db import get_db
from services.chat_Services import add_message, get_session_with_messages
from src.controller.ai_function import ask_question
from src.models.models  import ChatSessionOut, MessageCreate, QuestionResponse
from fastapi import APIRouter, Depends, FastAPI, HTTPException

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



@router.post("/ask/{session_id}", response_model=ChatSessionOut)
def ask(
    session_id: str,
    body: MessageCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)  ← add after auth is done
):
    user_id = "temp-user-id"   # replace with current_user.id after auth

    session = get_session_with_messages(db, session_id, user_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 1. Save the user message
    add_message(db, session_id, role="user", content=body.content, image_url=body.image_url)

    # 2. Build history for LangChain context
    history = [
        {"role": m.role, "content": m.content}
        for m in session.messages
    ]

    # 3. Call your AI
    ai_response = ask_question(history=history, question=body.content)

    # 4. Save assistant reply
    add_message(db, session_id, role="assistant", content=ai_response)

    # 5. Auto-title the session from first user message
    if not session.title:
        session.title = body.content[:80]
        db.commit()

    db.refresh(session)
    return session