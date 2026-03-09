from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint

from backend.app.db.base import Base


class Developer(Base):
    __tablename__ = "developers"
    __table_args__ = (UniqueConstraint("org_id", "external_id", name="uq_dev_org_external_id"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    # external_id is the id the agent/SDK uses (e.g. "dev_123")
    external_id = Column(String(200), nullable=False)
    email = Column(String(320), nullable=True)
    display_name = Column(String(200), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

