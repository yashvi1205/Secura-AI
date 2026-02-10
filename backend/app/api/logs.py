from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.threat_log import ThreatLog

router = APIRouter()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(ThreatLog).order_by(ThreatLog.created_at.desc()).all()
    return logs
