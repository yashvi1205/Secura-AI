from __future__ import annotations

from backend.app.schemas.mvp import PolicyRule, RuleCategory, RuleSeverity


POLICY_VERSION = "mvp-2026-03-06"


MVP_RULES: dict[str, PolicyRule] = {
    # Back-compat with current security_engine.py rule ids
    "malicious_keyword": PolicyRule(
        id="malicious_keyword",
        title="Potentially malicious intent keyword",
        category=RuleCategory.prompt,
        default_severity=RuleSeverity.high,
        description="Simple keyword detector for overt malicious requests (MVP heuristic).",
        references=[],
    ),
    "sensitive_keyword": PolicyRule(
        id="sensitive_keyword",
        title="Sensitive context keyword",
        category=RuleCategory.prompt,
        default_severity=RuleSeverity.medium,
        description="Simple keyword detector for sensitive targets (MVP heuristic).",
        references=[],
    ),
    # Forward-looking stable ids (not all are implemented yet)
    "secura.prompt.injection.v1": PolicyRule(
        id="secura.prompt.injection.v1",
        title="Prompt injection attempt",
        category=RuleCategory.prompt,
        default_severity=RuleSeverity.high,
        description="Detects attempts to override system policies or exfiltrate hidden instructions.",
        references=[],
    ),
    "secura.secrets.pattern.v1": PolicyRule(
        id="secura.secrets.pattern.v1",
        title="Secret/token pattern detected",
        category=RuleCategory.secrets,
        default_severity=RuleSeverity.critical,
        description="Detects API keys/tokens and high-confidence secret formats in content.",
        references=[],
    ),
    "secura.pii.pattern.v1": PolicyRule(
        id="secura.pii.pattern.v1",
        title="PII pattern detected",
        category=RuleCategory.pii,
        default_severity=RuleSeverity.high,
        description="Detects common PII patterns (email, phone, SSN-like).",
        references=[],
    ),
    "secura.exfil.destination.v1": PolicyRule(
        id="secura.exfil.destination.v1",
        title="Suspicious destination / exfil attempt",
        category=RuleCategory.exfiltration,
        default_severity=RuleSeverity.high,
        description="Detects attempts to send sensitive data to external destinations.",
        references=[],
    ),
}


MVP_NOTIFICATION_CHANNELS = ["email", "slack", "webhook", "in_app"]

