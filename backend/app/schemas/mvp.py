from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    # LLM lifecycle
    prompt_sent = "prompt_sent"
    response_received = "response_received"
    tool_invoked = "tool_invoked"

    # Developer/IDE activity
    file_changed = "file_changed"
    dependency_added = "dependency_added"
    git_push = "git_push"

    # CI / pipeline activity
    ci_job = "ci_job"

    # Security signals / detections
    secret_detected = "secret_detected"
    policy_violation = "policy_violation"


class EventSource(str, Enum):
    ide = "ide"
    sdk = "sdk"
    ci = "ci"
    server = "server"


class PolicyEnforcementMode(str, Enum):
    log = "log"
    warn = "warn"
    block = "block"


class RuleSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class RuleCategory(str, Enum):
    prompt = "prompt"
    secrets = "secrets"
    pii = "pii"
    exfiltration = "exfiltration"
    malware = "malware"
    system = "system"
    anomaly = "anomaly"
    compliance = "compliance"


class NotificationChannel(str, Enum):
    email = "email"
    slack = "slack"
    webhook = "webhook"
    in_app = "in_app"


class PolicyRule(BaseModel):
    id: str = Field(..., description="Stable rule identifier, e.g. secura.prompt.injection.v1")
    title: str
    category: RuleCategory
    default_severity: RuleSeverity
    description: Optional[str] = None
    references: List[str] = Field(default_factory=list)


class RuleHit(BaseModel):
    rule_id: str
    category: RuleCategory
    severity: RuleSeverity
    message: str
    score: int = Field(ge=0, le=100)
    meta: Dict[str, Any] = Field(default_factory=dict)


class PolicyDecision(BaseModel):
    policy_version: str
    enforcement_mode: PolicyEnforcementMode
    risk_score: int = Field(ge=0, le=100)
    risk_level: Literal["low", "medium", "high", "critical"]
    hits: List[RuleHit] = Field(default_factory=list)


class IngestEvent(BaseModel):
    """
    MVP ingest envelope used by agents/SDK/CI.
    Raw content should already be redacted on-device if configured.
    """

    org_id: str
    project_id: str
    developer_id: str
    timestamp: datetime
    event_type: EventType
    source: EventSource

    host_id: Optional[str] = None
    ip: Optional[str] = None
    trace_id: Optional[str] = None

    payload: Dict[str, Any] = Field(default_factory=dict)


class IngestBatch(BaseModel):
    org_id: str
    project_id: str
    developer_id: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    events: List[IngestEvent]

    # Agent-side signing (HMAC) for tamper resistance (implemented in later tasks).
    signature: Optional[str] = None
    signature_alg: Optional[Literal["hmac-sha256"]] = None

