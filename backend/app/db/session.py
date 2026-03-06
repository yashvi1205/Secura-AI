from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# Ensure models are imported so SQLAlchemy can register them for metadata/migrations.
from backend.app.models import threat_log  # noqa: F401


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()