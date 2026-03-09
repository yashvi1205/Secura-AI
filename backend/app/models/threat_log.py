from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Text, JSON
from datetime import datetime
from backend.app.db.base import Base

class ThreatLog(Base):
    __tablename__ = "threat_logs"

    __table_args__=(
        CheckConstraint(
             "risk_level IN ('low', 'medium', 'high')",
            name="risk_level_check"
        ),
         CheckConstraint(
            "action IN ('allowed', 'flagged', 'blocked')",
            name="action_check"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    risk_level = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    reasons = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    policy_version = Column(String, nullable=False)
    client_ip = Column(String, nullable=False)
    developer_id = Column(String, nullable=True)
    project = Column(String, nullable=True)
    model = Column(String, nullable=True)
    activity_type = Column(String, nullable=True)
    activity_meta = Column(JSON, nullable=True)


