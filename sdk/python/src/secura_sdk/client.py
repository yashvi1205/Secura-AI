from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, Optional

from secura_sdk.http import post_json
from secura_sdk.signing import hmac_sha256_b64


def _strip_trailing_slash(url: str) -> str:
    return (url or "").rstrip("/")


@dataclass(frozen=True)
class SecuraClient:
    api_base: str
    api_key: str

    developer_id: Optional[str] = None
    email: Optional[str] = None
    project: Optional[str] = None
    model: Optional[str] = None
    host_id: Optional[str] = None

    def ingest_batch(self, *, events: Iterable[Dict[str, Any]], sign: bool = False) -> Dict[str, Any]:
        events_list = list(events)
        body: Dict[str, Any] = {
            "sent_at": datetime.utcnow().isoformat(),
            "signature": None,
            "signature_alg": None,
            "events": events_list,
        }
        if sign:
            body["signature_alg"] = "hmac-sha256"
            body["signature"] = hmac_sha256_b64(self.api_key, body)

        res = post_json(
            f"{_strip_trailing_slash(self.api_base)}/ingest/events",
            headers={"X-Secura-Key": self.api_key},
            body=body,
        )
        if res.status == 0:
            raise RuntimeError(f"Secura ingest failed: {res.text}")
        if res.status >= 400:
            raise RuntimeError(f"Secura ingest failed ({res.status}): {res.text}")
        return res.json if isinstance(res.json, dict) else {"status": res.status, "raw": res.text}

    def ingest_event(
        self,
        *,
        event_type: str,
        source: str = "sdk",
        occurred_at: Optional[datetime] = None,
        trace_id: Optional[str] = None,
        session_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        event = {
            "event_type": event_type,
            "source": source,
            "occurred_at": (occurred_at or datetime.utcnow()).isoformat(),
            "actor": {"developer_id": self.developer_id, "email": self.email},
            "context": {
                "org_id": None,
                "project": self.project,
                "model": self.model,
                "host_id": self.host_id,
                "ip": None,
                "user_agent": None,
                "trace_id": trace_id,
                "session_id": session_id,
            },
            "data": data or {},
        }
        return self.ingest_batch(events=[event], sign=False)

    def ingest_prompt(
        self,
        prompt: str,
        *,
        trace_id: Optional[str] = None,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"prompt": prompt}
        if model or self.model:
            data["model"] = model or self.model
        if extra:
            data.update(extra)

        return self.ingest_event(
            event_type="prompt_sent",
            source="sdk",
            trace_id=trace_id,
            session_id=session_id,
            data=data,
        )

    def instrumented_call(
        self,
        *,
        prompt: str,
        call,
        trace_id: Optional[str] = None,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Minimal proxy wrapper: logs prompt_sent and response_received around a model call.

        `call` can be any callable that accepts a prompt and returns a response.
        """
        self.ingest_prompt(prompt, trace_id=trace_id, session_id=session_id, model=model, extra=extra)
        response = call(prompt)
        self.ingest_event(
            event_type="response_received",
            source="sdk",
            trace_id=trace_id,
            session_id=session_id,
            data={"response": str(response), "model": model or self.model},
        )
        return response

