from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.app.core.auth import require_api_key
from backend.app.core.queue import try_enqueue
from backend.app.db.session import get_db
from backend.app.models.api_key import ApiKey
from backend.app.models.developer import Developer
from backend.app.models.event import Event
from backend.app.models.project import Project
from backend.app.schemas.ingest import IngestBatch, IngestResponse
from backend.app.jobs.detections import process_events


router = APIRouter(prefix="/ingest", tags=["Ingest"])


def _get_or_create_project(db: Session, *, org_id: str, name: str | None) -> Project | None:
    if not name:
        return None
    p = db.query(Project).filter(Project.org_id == org_id, Project.name == name).first()
    if p:
        return p
    p = Project(org_id=org_id, name=name)
    db.add(p)
    db.flush()
    return p


def _get_or_create_developer(db: Session, *, org_id: str, external_id: str | None, email: str | None) -> Developer | None:
    if not external_id:
        return None
    d = db.query(Developer).filter(Developer.org_id == org_id, Developer.external_id == external_id).first()
    if d:
        if email and not d.email:
            d.email = email
            db.add(d)
        return d
    d = Developer(org_id=org_id, external_id=external_id, email=email)
    db.add(d)
    db.flush()
    return d


@router.post("/events", response_model=IngestResponse)
def ingest_events(
    batch: IngestBatch,
    http_request: Request,
    db: Session = Depends(get_db),
    api_key: ApiKey = Depends(require_api_key),
):
    org_id = api_key.org_id
    accepted = 0
    rejected = 0
    event_ids: list[int] = []

    ua = http_request.headers.get("user-agent")
    ip = http_request.client.host if http_request.client else None

    for e in batch.events:
        try:
            project = _get_or_create_project(db, org_id=org_id, name=e.context.project)
            dev = _get_or_create_developer(
                db,
                org_id=org_id,
                external_id=e.actor.developer_id,
                email=e.actor.email,
            )

            rec = Event(
                org_id=org_id,
                project_id=project.id if project else None,
                developer_id=dev.id if dev else None,
                event_type=e.event_type.value,
                source=e.source.value,
                occurred_at=e.occurred_at,
                received_at=datetime.utcnow(),
                host_id=e.context.host_id,
                ip=e.context.ip or ip,
                user_agent=e.context.user_agent or ua,
                trace_id=e.context.trace_id,
                session_id=e.context.session_id,
                payload=e.data,
            )
            db.add(rec)
            db.flush()
            if rec.id is not None:
                event_ids.append(int(rec.id))
            accepted += 1
        except Exception:
            rejected += 1

    db.commit()

    if event_ids:
        enqueued = try_enqueue(process_events, event_ids)
        if not enqueued:
            process_events(event_ids)

    return IngestResponse(accepted=accepted, rejected=rejected, server_time=datetime.utcnow())

