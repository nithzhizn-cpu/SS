from fastapi import FastAPI
from database import Base, engine
import routes_messages
import routes_calls

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes_messages.router)
app.include_router(routes_calls.router)

@app.get("/health")
def health():
    return {"status": "ok"}