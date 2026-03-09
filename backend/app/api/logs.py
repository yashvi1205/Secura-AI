from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.threat_log import ThreatLog
from backend.app.schemas.security import ThreatLogResponse

router = APIRouter()

@router.get("/logs", response_model=List[ThreatLogResponse])
def get_logs(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    risk_level: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    developer_id: Optional[str] = Query(None),
    project: Optional[str] = Query(None),
):
    q = db.query(ThreatLog)
    if risk_level:
        q = q.filter(ThreatLog.risk_level == risk_level)
    if action:
        q = q.filter(ThreatLog.action == action)
    if developer_id:
        q = q.filter(ThreatLog.developer_id == developer_id)
    if project:
        q = q.filter(ThreatLog.project == project)

    logs = q.order_by(ThreatLog.created_at.desc()).limit(limit).all()
    return [ThreatLogResponse.model_validate(l) for l in logs]
