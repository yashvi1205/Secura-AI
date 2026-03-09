from __future__ import annotations

import hashlib
import hmac


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def secure_eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

