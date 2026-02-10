POLICY_VERSION = "1.0.0"

from dataclasses import dataclass

HIGH_RISK_KEYWORDS = [
    "hack",
    "password",
    "exploit",
    "bypass"
]

MEDIUM_RISK_KEYWORDS = [
    "scan",
    "enumerate",
    "probe",
    "attack"
]


   
@dataclass
class SecurityDecision:
    risk_level:str
    action:str
    score:int
    reasons: list[str]
    policy_version: str

def analyze_prompt(prompt:str)->SecurityDecision:
     text = prompt.lower()

     if any(keyword in text for keyword in HIGH_RISK_KEYWORDS): 
          return SecurityDecision(
               risk_level="high",
               action="blocked",
               score=90,
               reasons=["Detected high-risk keyword"],
               policy_version="1.0.0"

          )
     
     elif any(keyword in text for keyword in MEDIUM_RISK_KEYWORDS):
          return SecurityDecision(
               risk_level="medium",
               action="review",
               score=60,
               reasons=["Detected suspicious keyword"],
               policy_version="1.0.0"

          )
     
     return SecurityDecision(
        risk_level="low",
        action="allowed",
        score=10,
        reasons=[],
        policy_version=POLICY_VERSION
    )

