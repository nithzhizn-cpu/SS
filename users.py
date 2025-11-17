from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import secrets

import models
import schemas

router = APIRouter(tags=["Users"])


# -----------------------------
# Register / Login
# -----------------------------
@router.post("/register", response_model=schemas.UserOut)
def register_user(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == req.username).first()

    if existing:
        return existing

    token = secrets.token_hex(32)

    user = models.User(
        username=req.username,
        telegram_id=req.telegram_id,
        token=token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -----------------------------
# Search users
# -----------------------------
@router.get("/users/search")
def search_users(query: str, db: Session = Depends(get_db)):
    q = query.strip()

    if not q:
        return {"results": []}

    results = []

    if q.isdigit():
        u = db.query(models.User).filter(models.User.id == int(q)).first()
        if u:
            results.append(u)

    by_name = (
        db.query(models.User)
        .filter(models.User.username.ilike(f"%{q}%"))
        .all()
    )

    for u in by_name:
        if u not in results:
            results.append(u)

    return {"results": [schemas.UserOut.model_validate(u) for u in results]}


# -----------------------------
# Save public E2EE key
# -----------------------------
@router.post("/pubkey")
def save_pubkey(
    req: schemas.PubKeyUpdate,
    user=Depends(models.get_current_user),
    db: Session = Depends(get_db)
):
    user.pubkey = req.pubkey
    db.commit()
    return {"ok": True}


# -----------------------------
# Get pubkey of user
# -----------------------------
@router.get("/pubkey/{user_id}")
def get_pubkey(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.pubkey:
        raise HTTPException(status_code=404, detail="No pubkey")
    return {"pubkey": user.pubkey}
