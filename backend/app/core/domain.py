from __future__ import annotations

from enum import Enum


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Action(str, Enum):
    allowed = "allowed"
    flagged = "flagged"
    blocked = "blocked"


class EventSource(str, Enum):
    ide = "ide"
    sdk = "sdk"
    ci = "ci"
    server = "server"


class EventType(str, Enum):
    # LLM / agent activity
    prompt_sent = "prompt_sent"
    response_received = "response_received"
    tool_invoked = "tool_invoked"

    # Dev activity signals
    file_changed = "file_changed"
    dependency_added = "dependency_added"
    git_push = "git_push"
    ci_job = "ci_job"

    # Security detections
    secret_detected = "secret_detected"
    policy_violation = "policy_violation"


class NotificationChannel(str, Enum):
    email = "email"
    slack = "slack"
    webhook = "webhook"

