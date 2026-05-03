from sqlalchemy.orm import Session
from src.schemas.schema import ChatSession, Message
import uuid

def create_session(db: Session, user_id: str, title: str | None = None) -> ChatSession:
    session = ChatSession(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_user_sessions(db: Session, user_id: str) -> list[ChatSession]:
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()

def get_session_with_messages(db: Session, session_id: str, user_id: str) -> ChatSession | None:
    return (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == user_id)
        .first()
    )

def add_message(db: Session, session_id: str, role: str, content: str, image_url: str | None = None) -> Message:
    msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role=role,
        content=content,
        image_url=image_url
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def delete_session(db: Session, session_id: str, user_id: str) -> bool:
    session = get_session_with_messages(db, session_id, user_id)
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True