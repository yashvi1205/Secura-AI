from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.session import get_db
from backend.app.models.threat_log import ThreatLog

router = APIRouter(prefix="/admin",tags=["Admin"])

@router.get("/summary")
def get_summary(db:Session=Depends(get_db)):
    total_requests=db.query(func.count(ThreatLog.id)).scalar()

    high_risk = db.query(func.count(ThreatLog.id))\
        .filter(ThreatLog.risk_level == "high")\
        .scalar()
    
    medium_risk = db.query(func.count(ThreatLog.id))\
        .filter(ThreatLog.risk_level == "medium")\
        .scalar()
    
    low_risk = db.query(func.count(ThreatLog.id))\
        .filter(ThreatLog.risk_level == "low")\
        .scalar()
    
    return {
        "total_requests": total_requests,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }