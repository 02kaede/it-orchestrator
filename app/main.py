from fastapi import FastAPI
from .core.logging import setup_logging
from .api.routes_chat import router as chat_router

setup_logging()

app = FastAPI(title="IT Support Orchestrator", version="0.1.0")
app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok"}

from .db.session import create_db

@app.on_event("startup")
def on_startup():
    create_db()