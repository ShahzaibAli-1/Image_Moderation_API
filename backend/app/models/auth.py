from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TokenCreate(BaseModel):
    is_admin: bool = False

class Token(BaseModel):
    token: str
    is_admin: bool
    created_at: datetime
    last_used: Optional[datetime] = None

class TokenResponse(BaseModel):
    token: str
    is_admin: bool
    created_at: datetime

class UsageRecord(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "success"
    details: Optional[dict] = None 