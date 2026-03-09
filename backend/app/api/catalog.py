from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.mvp_catalog import MVP_NOTIFICATION_CHANNELS, MVP_RULES, POLICY_VERSION


router = APIRouter(prefix="/mvp", tags=["MVP"])


@router.get("/catalog")
def get_mvp_catalog():
    return {
        "policy_version": POLICY_VERSION,
        "rules": [r.model_dump() for r in MVP_RULES.values()],
        "notification_channels": MVP_NOTIFICATION_CHANNELS,
    }

