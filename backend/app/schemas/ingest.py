from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.core.domain import EventSource, EventType


class EventActor(BaseModel):
    developer_id: Optional[str] = None
    email: Optional[str] = None


class EventContext(BaseModel):
    org_id: Optional[str] = None
    project: Optional[str] = None
    model: Optional[str] = None

    host_id: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None

    trace_id: Optional[str] = None
    session_id: Optional[str] = None


class IngestEvent(BaseModel):
    event_type: EventType
    source: EventSource = EventSource.sdk
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    actor: EventActor = Field(default_factory=EventActor)
    context: EventContext = Field(default_factory=EventContext)

    # Minimal payload, intentionally free-form for MVP.
    # Concrete schemas can be added per event_type later.
    data: Dict[str, Any] = Field(default_factory=dict)


class IngestBatch(BaseModel):
    events: List[IngestEvent] = Field(..., min_length=1, max_length=500)


class IngestResponse(BaseModel):
    accepted: int
    rejected: int
    server_time: datetime

