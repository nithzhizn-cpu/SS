from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.post("/call/offer")
def send_offer(data: dict, db: Session = Depends(get_db)):
    models.CallSignal.store("offer", data, db)
    return {"ok": True}

@router.post("/call/answer")
def send_answer(data: dict, db: Session = Depends(get_db)):
    models.CallSignal.store("answer", data, db)
    return {"ok": True}

@router.post("/call/candidate")
def send_candidate(data: dict, db: Session = Depends(get_db)):
    models.CallSignal.store("candidate", data, db)
    return {"ok": True}

@router.get("/call/poll")
def poll_signals(last_id: int = 0, db: Session = Depends(get_db)):
    return models.CallSignal.poll(last_id, db)
