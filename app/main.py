from __future__ import annotations

from fastapi import FastAPI

from app.routes.chat import router as chat_router

app = FastAPI(title="StayEase AI Agent", version="1.0.0")
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])


@app.get("/")
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok", "service": "StayEase AI Agent"}
