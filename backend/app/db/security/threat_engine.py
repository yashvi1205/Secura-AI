from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from backend.app.core.security_engine import analyze_prompt
from backend.app.core.security_config import POLICY_VERSION
from backend.app.models.threat_log import ThreatLog


def analyze_and_log(
    *,
    prompt: str,
    db: Session,
    client_ip: str,
    developer_id: Optional[str] = None,
    project: Optional[str] = None,
    model: Optional[str] = None,
    activity_type: Optional[str] = None,
    activity_meta: Optional[Dict[str, Any]] = None,
):
    result = analyze_prompt(prompt)
    log = ThreatLog(
        prompt=prompt,
        risk_level=result["risk_level"],
        score=result["score"],
        action=result["action"],
        reasons=result["reasons"],
        policy_version=POLICY_VERSION,
        client_ip=client_ip,
        developer_id=developer_id,
        project=project,
        model=model,
        activity_type=activity_type,
        activity_meta=activity_meta,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return result, log

