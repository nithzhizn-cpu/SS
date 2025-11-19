from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str

class PubKeyRequest(BaseModel):
    pubkey: str

class SendMessageRequest(BaseModel):
    to: int
    iv: str
    ciphertext: str

class CallOffer(BaseModel):
    caller_id: int
    receiver_id: int
    sdp: str

class CallAnswer(BaseModel):
    caller_id: int
    receiver_id: int
    sdp: str

class CallCandidate(BaseModel):
    caller_id: int
    receiver_id: int
    candidate: str
