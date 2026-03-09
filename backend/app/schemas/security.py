from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RuleReason(BaseModel):
    rule_id: str
    category: str
    severity: str
    message: str
    score: int


class SecureRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    developer_id: Optional[str] = None
    project: Optional[str] = None
    model: Optional[str] = None
    activity_type: Optional[str] = None
    activity_meta: Optional[Dict[str, Any]] = None


class SecureResponse(BaseModel):
    risk_level: str
    score: int
    action: str
    reasons: List[RuleReason]
    policy_version: str


class ThreatLogResponse(BaseModel):
    id: int
    prompt: str
    risk_level: str
    score: int
    action: str
    reasons: List[Dict[str, Any]] | List[RuleReason] | None
    policy_version: str
    created_at: datetime
    client_ip: str
    developer_id: Optional[str] = None
    project: Optional[str] = None
    model: Optional[str] = None
    activity_type: Optional[str] = None
    activity_meta: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
