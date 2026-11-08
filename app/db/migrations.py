from pathlib import Path
import logging
from sqlalchemy import text
from app.db.session import engine

logger = logging.getLogger(__name__)
MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"

def apply_migrations() -> None:
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(100) PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
        for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            version = migration_file.name
            exists = connection.execute(
                text("SELECT 1 FROM schema_migrations WHERE version = :version"),
                {"version": version},
            ).first()
            if exists:
                continue
            connection.exec_driver_sql(migration_file.read_text(encoding="utf-8"))
            connection.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": version},
            )
            logger.info("Applied migration %s", version)
