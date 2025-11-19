from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/messages")
def send_message(msg: schemas.MessageCreate,
                 current=Depends(models.get_current_user),
                 db: Session = Depends(get_db)):
    
    peer = db.query(models.User).filter(models.User.id == msg.to).first()

    if not peer:
        raise HTTPException(404, "Recipient not found")

    db_msg = models.Message(
        from_id=current.id,
        to_id=peer.id,
        iv=msg.iv,
        ciphertext=msg.ciphertext,
        msg_type=msg.msg_type,
        ttl_sec=msg.ttl_sec
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    return {"ok": True, "id": db_msg.id}
