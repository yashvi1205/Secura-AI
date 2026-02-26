from pydantic import BaseModel
from typing import List
from datetime import datetime


class ThreatLogResponse(BaseModel):
    id: int
    prompt: str
    risk_level: str
    score: int
    action: str
    reasons: List[RuleReason]
    policy_version: str
    created_at: datetime

    class Config:
        from_attributes = True


class SecureRequest(BaseModel):
    prompt: str
class RuleReason(BaseModel):
    rule_id: str
    category: str
    severity: str
    message: str
    score: int
class SecureResponse(BaseModel):
    risk_level: str
    score: int
    action: str
    reasons: List[RuleReason]
    policy_version: str
