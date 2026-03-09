from __future__ import annotations

import secrets
from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.crypto import sha256_hex
from backend.app.db.session import get_db
from backend.app.models.api_key import ApiKey


def _extract_api_key(
    authorization: Optional[str],
    x_secura_key: Optional[str],
) -> Optional[str]:
    if x_secura_key and x_secura_key.strip():
        return x_secura_key.strip()
    if authorization and authorization.strip().lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    return None


def create_api_key_secret() -> str:
    # human-friendly-ish, URL-safe
    return "sec_" + secrets.token_urlsafe(32)


def api_key_prefix(secret_value: str) -> str:
    raw = (secret_value or "").strip()
    return raw[:12]


def hash_api_key(secret_value: str) -> str:
    return sha256_hex(secret_value.strip())


def require_api_key(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None),
    x_secura_key: Optional[str] = Header(default=None, alias="X-Secura-Key"),
):
    secret_value = _extract_api_key(authorization, x_secura_key)
    if not secret_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    key_hash = hash_api_key(secret_value)
    rec = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
    if not rec or rec.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    rec.last_used_at = datetime.utcnow()
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

