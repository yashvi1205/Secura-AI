from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.core.auth import require_api_key
from backend.app.db.session import get_db
from backend.app.models.api_key import ApiKey
from backend.app.models.detection import Detection
from backend.app.models.event import Event
from backend.app.models.incident import Incident
from backend.app.schemas.console import DetectionOut, EventOut, IncidentOut


router = APIRouter(prefix="/console", tags=["Console"])


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(require_api_key),
):
    org_id = api_key.org_id
    total_events = db.query(func.count(Event.id)).filter(Event.org_id == org_id).scalar() or 0
    total_detections = db.query(func.count(Detection.id)).filter(Detection.org_id == org_id).scalar() or 0

    high = db.query(func.count(Detection.id)).filter(Detection.org_id == org_id, Detection.risk_level == "high").scalar() or 0
    med = db.query(func.count(Detection.id)).filter(Detection.org_id == org_id, Detection.risk_level == "medium").scalar() or 0
    low = db.query(func.count(Detection.id)).filter(Detection.org_id == org_id, Detection.risk_level == "low").scalar() or 0

    open_incidents = db.query(func.count(Incident.id)).filter(Incident.org_id == org_id, Incident.status == "open").scalar() or 0

    return {
        "total_events": total_events,
        "total_detections": total_detections,
        "detections": {"high": high, "medium": med, "low": low},
        "open_incidents": open_incidents,
    }


@router.get("/events", response_model=list[EventOut])
def list_events(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(require_api_key),
    limit: int = Query(100, ge=1, le=500),
    cursor: int | None = Query(None, description="Fetch events with id < cursor"),
    event_type: str | None = Query(None),
):
    q = db.query(Event).filter(Event.org_id == api_key.org_id)
    if cursor:
        q = q.filter(Event.id < cursor)
    if event_type:
        q = q.filter(Event.event_type == event_type)
    rows = q.order_by(Event.id.desc()).limit(limit).all()
    return [EventOut.model_validate(r, from_attributes=True) for r in rows]


@router.get("/detections", response_model=list[DetectionOut])
def list_detections(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(require_api_key),
    limit: int = Query(100, ge=1, le=500),
    cursor: int | None = Query(None, description="Fetch detections with id < cursor"),
    risk_level: str | None = Query(None),
    action: str | None = Query(None),
):
    q = db.query(Detection).filter(Detection.org_id == api_key.org_id)
    if cursor:
        q = q.filter(Detection.id < cursor)
    if risk_level:
        q = q.filter(Detection.risk_level == risk_level)
    if action:
        q = q.filter(Detection.action == action)
    rows = q.order_by(Detection.id.desc()).limit(limit).all()
    return [DetectionOut.model_validate(r, from_attributes=True) for r in rows]


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(require_api_key),
    limit: int = Query(100, ge=1, le=500),
    cursor: int | None = Query(None, description="Fetch incidents with id < cursor"),
    status: str | None = Query(None),
):
    q = db.query(Incident).filter(Incident.org_id == api_key.org_id)
    if cursor:
        q = q.filter(Incident.id < cursor)
    if status:
        q = q.filter(Incident.status == status)
    rows = q.order_by(Incident.id.desc()).limit(limit).all()
    return [IncidentOut.model_validate(r, from_attributes=True) for r in rows]

