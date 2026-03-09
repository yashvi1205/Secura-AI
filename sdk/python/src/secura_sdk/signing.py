from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any, Dict


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hmac_sha256_b64(secret: str, payload: Dict[str, Any]) -> str:
    msg = canonical_json(payload)
    digest = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")

