from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# Ensure models are imported so SQLAlchemy can register them for metadata/migrations.
from backend.app.models import (  # noqa: F401
    api_key,
    developer,
    detection,
    event,
    incident,
    notification,
    org,
    project,
    threat_log,
)


_connect_args = {}
if settings.database_url.startswith("postgresql"):
    _connect_args["connect_timeout"] = 5
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()