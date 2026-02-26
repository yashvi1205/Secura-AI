from backend.app.core.security_config import MAX_RISK_SCORE, MEDIUM_RISK_SCORE
from backend.app.core.security_config import POLICY_VERSION

print(POLICY_VERSION)
print("policy_version" ,POLICY_VERSION)

def analyze_prompt(prompt: str):
    text = prompt.lower()
    score = 0
    reasons=[]
    malicious_keywords = [
        "hack", "bypass", "crack", "exploit",
        "attack", "steal", "override", "breach"
    ]

    sensitive_keywords = [
        "admin", "password", "database",
        "server", "login", "credentials", "token"
    ]

    for word in malicious_keywords:
        if word in text:
            score += 2

    for word in sensitive_keywords:
        if word in text:
            score += 2
            reasons.append({
                "rule": "sensitive_keyword",
                "message": f"Matched keyword: {word}",
                 "score": 2
            })

    if score >= MAX_RISK_SCORE:
        risk = "high"
        action = "blocked"
    elif score >= MEDIUM_RISK_SCORE:
        risk = "medium"
        action = "flagged"
    else:
        risk = "low"
        action = "allowed"

    return {
    "risk": risk,
    "score": score,
    "action": action,
    "reasons":reasons,
    "policy_version": POLICY_VERSION
}