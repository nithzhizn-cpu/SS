from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    token = Column(String, unique=True)
    pubkey = Column(Text, nullable=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    iv = Column(String)
    ciphertext = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CallSignal(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    caller_id = Column(Integer)
    receiver_id = Column(Integer)
    type = Column(String)   # offer / answer / candidate
    data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())