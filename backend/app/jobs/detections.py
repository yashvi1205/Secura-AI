from __future__ import annotations

from datetime import datetime
from typing import Iterable, List

from sqlalchemy.orm import Session

from backend.app.core.security_config import POLICY_VERSION
from backend.app.core.security_engine import analyze_prompt
from backend.app.db.session import SessionLocal
from backend.app.models.detection import Detection
from backend.app.models.event import Event
from backend.app.models.incident import Incident


def _ensure_incident(db: Session, *, org_id: str, event: Event, detection: Detection) -> Incident:
    # MVP grouping heuristic: group by trace_id if present, else one incident per event for medium+.
    if event.trace_id:
        existing = (
            db.query(Incident)
            .filter(Incident.org_id == org_id, Incident.status == "open")
            .filter(Incident.summary.like(f"%trace_id={event.trace_id}%"))
            .order_by(Incident.created_at.desc())
            .first()
        )
        if existing:
            existing.last_event_id = event.id
            existing.updated_at = datetime.utcnow()
            db.add(existing)
            return existing

    inc = Incident(
        org_id=org_id,
        status="open",
        severity="high" if detection.risk_level in {"high"} else "medium",
        title=f"Policy violation: {detection.risk_level}",
        summary=f"event_id={event.id} trace_id={event.trace_id or '-'}",
        first_event_id=event.id,
        last_event_id=event.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(inc)
    db.flush()
    return inc


def process_events(event_ids: Iterable[int]) -> dict:
    ids: List[int] = [int(x) for x in event_ids]
    if not ids:
        return {"processed": 0}

    db = SessionLocal()
    processed = 0
    created_detections = 0
    created_incidents = 0
    try:
        events = db.query(Event).filter(Event.id.in_(ids)).all()
        for ev in events:
            processed += 1
            if ev.event_type != "prompt_sent":
                continue

            prompt = None
            if isinstance(ev.payload, dict):
                prompt = ev.payload.get("prompt") or ev.payload.get("text")
            if not prompt:
                continue

            result = analyze_prompt(str(prompt))
            det = Detection(
                org_id=ev.org_id,
                event_id=ev.id,
                policy_version=POLICY_VERSION,
                risk_level=result["risk_level"],
                score=int(result["score"]),
                action=str(result["action"]),
                hits=result.get("reasons") or [],
                created_at=datetime.utcnow(),
            )
            db.add(det)
            created_detections += 1

            if det.risk_level in {"medium", "high"}:
                _ensure_incident(db, org_id=ev.org_id, event=ev, detection=det)
                created_incidents += 1

        db.commit()
        return {
            "processed": processed,
            "detections": created_detections,
            "incidents": created_incidents,
        }
    finally:
        db.close()

