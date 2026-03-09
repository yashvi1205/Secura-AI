from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from backend.app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    developer_id = Column(String(36), ForeignKey("developers.id", ondelete="SET NULL"), nullable=True, index=True)

    event_type = Column(String(64), nullable=False, index=True)
    source = Column(String(32), nullable=False, index=True)

    occurred_at = Column(DateTime, nullable=False, index=True)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    host_id = Column(String(200), nullable=True, index=True)
    ip = Column(String(64), nullable=True, index=True)
    user_agent = Column(String(400), nullable=True)
    trace_id = Column(String(200), nullable=True, index=True)
    session_id = Column(String(200), nullable=True, index=True)

    payload = Column(JSON, nullable=False, default=dict)

