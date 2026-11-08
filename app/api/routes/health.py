from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import engine

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok", "service": "cryptopilot-api"}

@router.get("/ready")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except SQLAlchemyError:
        return {"status": "not_ready", "database": "unavailable"}
