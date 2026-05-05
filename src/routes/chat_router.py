from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.models import ChatSessionCreate, ChatSessionOut
from src.services.chat_Services import get_or_create_session, delete_session, get_session_with_messages, get_user_sessions
from src.config.db import get_db


router = APIRouter(prefix="/chat", tags=["Chat"])

# POST /chat/sessions → start a new session
@router.post("/sessions", response_model=ChatSessionOut)
def new_session(
    body: ChatSessionCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)  ← uncomment after auth
):
    user_id = "temp-user-id"   # replace after auth
    return get_or_create_session(db, user_id=user_id, title=body.title)

# GET /chat/sessions → list all sessions for the user
@router.get("/sessions", response_model=list[ChatSessionOut])
def list_sessions(
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"
    return get_user_sessions(db, user_id)

# GET /chat/sessions/{id} → full session with all messages (history)
@router.get("/sessions/{session_id}", response_model=ChatSessionOut)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"
    session = get_session_with_messages(db, session_id, user_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# DELETE /chat/sessions/{id} → delete session + all its messages (cascade)
@router.delete("/sessions/{session_id}")
def remove_session(
    session_id: str,
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"
    ok = delete_session(db, session_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"detail": "Session deleted"}


@router.delete("/sessions/delateAll/{session_id}")
def remove_session(
    session_id: str,
    db: Session = Depends(get_db),
):
    user_id = "temp-user-id"
    ok = delete_session(db, session_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"detail": "Session deleted"}