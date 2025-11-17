from fastapi import FastAPI
from database import Base, engine

# Імпорт роутерів
from routes.users import router as users_router
from routes.messages import router as messages_router
from routes.calls import router as calls_router

# Створення таблиць
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpySignal Backend")

# Підключення роутів
app.include_router(users_router, prefix="/api")
app.include_router(messages_router, prefix="/api")
app.include_router(calls_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
