from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.schemas.security import SecureRequest, SecureResponse
from backend.app.models.threat_log import ThreatLog
from backend.app.core.security_engine import analyze_prompt  
from backend.app.core.security_config import POLICY_VERSION



router = APIRouter()


@router.post("/secure", response_model=SecureResponse)
def secure_prompt(
    request: SecureRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    user_prompt = request.prompt
    client_ip = http_request.client.host
    result = analyze_prompt(user_prompt)

    risk_level = result["risk_level"]
    score = result["score"]
    action = result["action"]
    reasons = result["reasons"]
    log = ThreatLog(
        prompt=user_prompt,
        risk_level=risk_level,
        score=score,
        action=action,
        reasons=reasons,
        policy_version=POLICY_VERSION,
        client_ip=client_ip,
        developer_id=request.developer_id,
        project=request.project,
        model=request.model,
        activity_type=request.activity_type,
        activity_meta=request.activity_meta,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return SecureResponse(
        risk_level=risk_level,
        score=score,
        action=action,
        reasons=reasons,             
        policy_version=POLICY_VERSION
    )