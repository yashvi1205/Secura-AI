from pydantic import BaseModel

class SecureRequest(BaseModel):
    prompt: str

class SecureResponse(BaseModel):
    risk_level: str
    action: str
    score:int
    reasons:list[str]

class ThreatLogResponse(BaseModel):
    id: int
    prompt: str
    risk_level: str
    score: int
    action: str
    reasons: list[str]
    created_at: str

    class Config:
        orm_mode = True

