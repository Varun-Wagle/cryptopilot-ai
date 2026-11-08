import logging
from fastapi import FastAPI
from app.api.routes import health, wallets
from app.core.config import settings
from app.db.migrations import apply_migrations

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Phase 1 foundation for a multi-chain crypto opportunity and earnings platform.",
    version="0.1.0",
)

@app.on_event("startup")
def startup_event():
    apply_migrations()

app.include_router(health.router)
app.include_router(wallets.router)

@app.get("/")
def root():
    return {"name": settings.app_name, "version": "0.1.0", "environment": settings.app_env, "docs": "/docs"}
