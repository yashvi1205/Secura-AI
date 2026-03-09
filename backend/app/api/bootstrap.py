from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.auth import api_key_prefix, create_api_key_secret, hash_api_key
from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.api_key import ApiKey
from backend.app.models.org import Organization


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/bootstrap")
def bootstrap(
    db: Session = Depends(get_db),
    x_bootstrap_token: Optional[str] = Header(default=None, alias="X-Bootstrap-Token"),
):
    if not settings.bootstrap_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bootstrap disabled")
    if not x_bootstrap_token or x_bootstrap_token != settings.bootstrap_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bootstrap token")

    org = db.query(Organization).filter(Organization.name == "default").first()
    if not org:
        org = Organization(name="default")
        db.add(org)
        db.commit()
        db.refresh(org)

    secret_value = create_api_key_secret()
    rec = ApiKey(
        org_id=org.id,
        name=f"bootstrap-{datetime.utcnow().isoformat(timespec='seconds')}",
        prefix=api_key_prefix(secret_value),
        key_hash=hash_api_key(secret_value),
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    return {
        "org_id": org.id,
        "api_key": secret_value,  # shown once
        "prefix": rec.prefix,
        "created_at": rec.created_at,
    }

