

from typing import Optional
import uuid

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.helper import access_token, get_current_user
from src.schemas.schema import ChatSession
from src.config.db import get_db
from src.services.chat_Services import add_message, generate_title, get_or_create_session, get_session_with_messages
from src.controller.ai_function import ask_question, ask_with_image
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
    content: str = Form(...),
    image: Optional[UploadFile] = File(default=None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    image_url = None

    if image and image.filename:
        # 1. Save to Cloudinary
        image_url = upload_to_cloudinary(image)

        # 2. Reset file pointer and call vision AI
        image.file.seek(0)                              # ← reset after cloudinary upload
        ai_response = ask_with_image(content, image.file)  # ← vision response
    else:
        # 3. Normal text question
        ai_response = ask_question(question=content)

    # 4. Auto-create session
    session = get_or_create_session(user_id, content, db)

    # 5. Save messages
    add_message(db, session.id, role="user", content=content, image_url=image_url)
    add_message(db, session.id, role="assistant", content=ai_response)

    return {
        "session_id": session.id,
        "title": session.title,
        "answer": ai_response,
        "image_url": image_url
    }

@router.post("/ask/{session_id}")
def ask_followup(
    session_id: str,
    content: str = Form(...),
    image: Optional[UploadFile] = File(default=None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    user_id = current_user.id
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 1. Save user message to DB first
    image_url = None
    if image and image.filename:
        image_url = upload_to_cloudinary(image)
    
    add_message(db, session_id, role="user", content=content, image_url=image_url)

    # 2. Build history
    history = [{"role": m.role, "content": m.content} for m in session.messages]

    # 3. Call AI ONLY ONCE
    if image and image.filename:
        image.file.seek(0)
        # Note: Make sure ask_with_image handles history if you want it to!
        ai_response = ask_with_image(content, image.file) 
    else:
        # This is where history is used
        ai_response = ask_question(question=content, history=history)

    # 4. Save assistant reply
    add_message(db, session_id, role="assistant", content=ai_response)

    return {
        "session_id": session_id,
        "answer": ai_response
    }
