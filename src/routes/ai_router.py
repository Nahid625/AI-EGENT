

from typing import Optional
import uuid

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.schemas.schema import ChatSession
from src.config.db import get_db
from src.services.chat_Services import add_message, get_or_create_session, get_session_with_messages
from src.controller.ai_function import ask_question
from src.models.models  import ChatSessionOut, MessageCreate, QuestionResponse
from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, UploadFile

from src.tools.uplaod import upload_to_cloudinary

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



@router.post("/ask")
def ask(
    content: str,                                          # ← plain form field, no body model
    image: Optional[UploadFile] = File(default=None),     # ← optional file
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)  ← add after auth
):
    user_id = "temp-user-id"

    # 1. Upload to Cloudinary if image provided, get back the secure_url
    image_url = None
    if image:
        image_url = upload_to_cloudinary(image)   # returns "https://res.cloudinary.com/..."

    # 2. Auto-create session with question as title
    session = get_or_create_session(db, user_id, content)

    # 3. Save user message + image url
    add_message(db, session.id, role="user", content=content, image_url=image_url)

    # 4. Call AI
    ai_response = ask_question(question=content)

    # 5. Save assistant reply
    add_message(db, session.id, role="assistant", content=ai_response)

    return {
        "session_id": session.id,
        "title": session.title,
        "answer": ai_response,
        "image_url": image_url        # None if no image was sent
    }

@router.post("/ask/{session_id}")
def ask_followup(
    session_id: str,
    body: MessageCreate,
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"

    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    add_message(db, session_id, role="user", content=body.content)

    # Build history for context
    history = [{"role": m.role, "content": m.content} for m in session.messages]

    # Call AI with full history
    ai_response = ask_question(question=body.content, history=history)

    # Save reply
    add_message(db, session_id, role="assistant", content=ai_response)

    return {
        "session_id": session_id,
        "answer": ai_response
    }@router.post("/ask")


def ask(
    content: str = Form(...),                          # ← Form() required for multipart
    image: Optional[UploadFile] = File(default=None),
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"

    image_url = None
    if image and image.filename:                       # ← guard against empty file
        image_url = upload_to_cloudinary(image)

    session = get_or_create_session(db, user_id, content)

    add_message(db, session.id, role="user", content=content, image_url=image_url)

    ai_response = ask_question(question=content)      # ← now returns plain string

    add_message(db, session.id, role="assistant", content=ai_response)  # ← string ✅

    return {
        "session_id": session.id,
        "title": session.title,
        "question": content,
        "answer": ai_response,
        "image_url": image_url
    }
@router.post("/ask/{session_id}")
def ask_followup(
    session_id: str,
    body: MessageCreate,
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"

    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    add_message(db, session_id, role="user", content=body.content)

    # Build history for context
    history = [{"role": m.role, "content": m.content} for m in session.messages]

    # Call AI with full history
    ai_response = ask_question(question=body.content, history=history)

    # Save reply
    add_message(db, session_id, role="assistant", content=ai_response)

    return {
        "session_id": session_id,
        "answer": ai_response
    }