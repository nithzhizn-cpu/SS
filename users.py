from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, secrets

router = APIRouter()

@router.post("/register")
def register_user(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == req.username).first()
    
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "token": user.token
        }
    
    token = secrets.token_hex(32)

    new_user = models.User(
        username=req.username,
        telegram_id=req.telegram_id,
        token=token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "token": new_user.token
    }
