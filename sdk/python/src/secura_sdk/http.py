from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class HttpResponse:
    status: int
    json: Dict[str, Any] | list | None
    text: str


def post_json(url: str, *, headers: Dict[str, str], body: Dict[str, Any]) -> HttpResponse:
    data = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    req = Request(url, method="POST", data=data)
    req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        with urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            parsed: Optional[Dict[str, Any] | list] = None
            try:
                parsed = json.loads(raw) if raw else None
            except Exception:
                parsed = None
            return HttpResponse(status=getattr(resp, "status", 200), json=parsed, text=raw)
    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        try:
            parsed = json.loads(raw) if raw else None
        except Exception:
            parsed = None
        return HttpResponse(status=int(getattr(e, "code", 500)), json=parsed, text=raw)
    except URLError as e:
        return HttpResponse(status=0, json=None, text=str(e))

