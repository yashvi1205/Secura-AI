from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from backend.app.db.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String(32), nullable=False, default="open", index=True)  # open|ack|resolved
    severity = Column(String(16), nullable=False, default="medium", index=True)  # low|medium|high|critical

    title = Column(String(240), nullable=False)
    summary = Column(Text, nullable=True)

    first_event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True)
    last_event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

