from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from backend.app.db.base import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)

    policy_version = Column(String(64), nullable=False)
    risk_level = Column(String(16), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    action = Column(String(16), nullable=False, index=True)
    hits = Column(JSON, nullable=False, default=list)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

