from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CallSignal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/call/offer")
def call_offer(data: dict, db: Session = Depends(get_db)):
    s = CallSignal(
        caller_id=data["caller_id"],
        receiver_id=data["receiver_id"],
        type="offer",
        data=data["sdp"]
    )
    db.add(s)
    db.commit()
    return {"status": "ok"}


@router.post("/call/answer")
def call_answer(data: dict, db: Session = Depends(get_db)):
    s = CallSignal(
        caller_id=data["caller_id"],
        receiver_id=data["receiver_id"],
        type="answer",
        data=data["sdp"]
    )
    db.add(s)
    db.commit()
    return {"status": "ok"}


@router.post("/call/candidate")
def call_candidate(data: dict, db: Session = Depends(get_db)):
    s = CallSignal(
        caller_id=data["caller_id"],
        receiver_id=data["receiver_id"],
        type="candidate",
        data=data["candidate"]
    )
    db.add(s)
    db.commit()
    return {"status": "ok"}


@router.get("/call/poll")
def poll(receiver_id: int, db: Session = Depends(get_db)):
    signals = db.query(CallSignal).filter(CallSignal.receiver_id == receiver_id).all()

    out = []
    for s in signals:
        out.append({
            "type": s.type,
            "caller_id": s.caller_id,
            "data": s.data
        })
        db.delete(s)

    db.commit()
    return {"signals": out}