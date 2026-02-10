from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.schemas.security import SecureRequest, SecureResponse
from backend.app.models.threat_log import ThreatLog
from backend.app.core.security_engine import analyze_prompt
from backend.app.schemas.security import ThreatLogResponse



router= APIRouter()

@router.post("/secure", response_model=SecureResponse)
def secure_prompt(
    request: SecureRequest,
    db: Session = Depends(get_db)
):
    decision = analyze_prompt(request.prompt)

    log = ThreatLog(
        prompt=request.prompt,
        risk_level=decision.risk_level,
        score=decision.score,
        action=decision.action,
        reasons=decision.reasons,
        policy_version=decision.policy_version,

    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return SecureResponse(
        risk_level=decision.risk_level,
        score=decision.score,
        action=decision.action,
        reasons=decision.reasons,
        policy_version=decision.policy_version
    )




