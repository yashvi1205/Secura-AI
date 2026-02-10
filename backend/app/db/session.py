from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.base import Base
from backend.app.models import threat_log

DATABASE_URL = "postgresql://postgres:121205@localhost:5432/secura_ai"
engine = create_engine(DATABASE_URL) #opens the connection pipeline
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )    #creates the session when needed


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()