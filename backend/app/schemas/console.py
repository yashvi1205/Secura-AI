from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class EventOut(BaseModel):
    id: int
    org_id: str
    project_id: Optional[str] = None
    developer_id: Optional[str] = None
    event_type: str
    source: str
    occurred_at: datetime
    received_at: datetime
    host_id: Optional[str] = None
    ip: Optional[str] = None
    trace_id: Optional[str] = None
    session_id: Optional[str] = None
    payload: Dict[str, Any]


class DetectionOut(BaseModel):
    id: int
    org_id: str
    event_id: int
    policy_version: str
    risk_level: str
    score: int
    action: str
    hits: List[Dict[str, Any]]
    created_at: datetime


class IncidentOut(BaseModel):
    id: int
    org_id: str
    status: str
    severity: str
    title: str
    summary: Optional[str] = None
    first_event_id: Optional[int] = None
    last_event_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class ListResponse(BaseModel):
    items: list
    next_cursor: Optional[int] = None

