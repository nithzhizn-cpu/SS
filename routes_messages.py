from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Message
from schemas import SendMessageRequest
import secrets

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth_user(db: Session, token: str):
    return db.query(User).filter(User.token == token).first()


@router.post("/api/messages")
def send_message(req: SendMessageRequest, Authorization: str = Header(...), db: Session = Depends(get_db)):
    user = auth_user(db, Authorization.replace("Bearer ", ""))
    if not user:
        return {"error": "invalid token"}

    message = Message(
        from_id=user.id,
        to_id=req.to,
        iv=req.iv,
        ciphertext=req.ciphertext,
    )
    db.add(message)
    db.commit()
    return {"status": "ok"}


@router.get("/api/messages")
def get_messages(peer_id: int, Authorization: str = Header(...), db: Session = Depends(get_db)):
    user = auth_user(db, Authorization.replace("Bearer ", ""))
    if not user:
        return {"messages": []}

    msgs = db.query(Message).filter(
        ((Message.from_id == user.id) & (Message.to_id == peer_id)) |
        ((Message.from_id == peer_id) & (Message.to_id == user.id))
    ).order_by(Message.created_at).all()

    return {"messages": [
        {
            "from_id": m.from_id,
            "to": m.to_id,
            "iv": m.iv,
            "ciphertext": m.ciphertext,
            "created_at": m.created_at
        }
        for m in msgs
    ]}