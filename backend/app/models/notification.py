from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from backend.app.db.base import Base


class NotificationDestination(Base):
    __tablename__ = "notification_destinations"

    id = Column(Integer, primary_key=True)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    channel = Column(String(24), nullable=False, index=True)  # email|slack|webhook|in_app
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)  # email addr or webhook url or slack webhook url
    enabled = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True, index=True)

    destination_id = Column(Integer, ForeignKey("notification_destinations.id", ondelete="SET NULL"), nullable=True)
    channel = Column(String(24), nullable=False, index=True)
    status = Column(String(24), nullable=False, default="queued", index=True)  # queued|sent|failed
    error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    sent_at = Column(DateTime, nullable=True)

