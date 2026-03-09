from __future__ import annotations

from backend.app.core.security_config import MAX_RISK_SCORE, MEDIUM_RISK_SCORE, POLICY_VERSION


def _reason(rule_id: str, *, category: str, severity: str, message: str, score: int):
    return {
        "rule_id": rule_id,
        "category": category,
        "severity": severity,
        "message": message,
        "score": score,
    }


def analyze_prompt(prompt: str):
    text = (prompt or "").lower()
    score = 0
    reasons = []

    malicious_keywords = [
        "hack",
        "bypass",
        "crack",
        "exploit",
        "attack",
        "steal",
        "override",
        "breach",
    ]

    sensitive_keywords = [
        "admin",
        "password",
        "database",
        "server",
        "login",
        "credentials",
        "token",
    ]

    for word in malicious_keywords:
        if word in text:
            score += 2
            reasons.append(
                _reason(
                    "malicious_keyword",
                    category="prompt",
                    severity="high",
                    message=f"Matched potentially malicious keyword: {word}",
                    score=2,
                )
            )

    for word in sensitive_keywords:
        if word in text:
            score += 2
            reasons.append(
                _reason(
                    "sensitive_keyword",
                    category="prompt",
                    severity="medium",
                    message=f"Matched sensitive keyword: {word}",
                    score=2,
                )
            )

    if score >= MAX_RISK_SCORE:
        risk_level = "high"
        action = "blocked"
    elif score >= MEDIUM_RISK_SCORE:
        risk_level = "medium"
        action = "flagged"
    else:
        risk_level = "low"
        action = "allowed"

    return {
        "risk_level": risk_level,
        "score": score,
        "action": action,
        "reasons": reasons,
        "policy_version": POLICY_VERSION,
    }