from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CostItem(BaseModel):
    name: str
    total: float

class MemberInput(BaseModel):
    name: str
    amount: float

class CreateSessionRequest(BaseModel):
    name: str
    cost_items: list[CostItem] = []
    members: list[MemberInput]

class ConfirmRequest(BaseModel):
    member_name: str

class MemberOut(BaseModel):
    name: str
    amount: float
    confirmed: bool = False
    confirmed_at: Optional[datetime] = None

class SessionOut(BaseModel):
    id: str
    name: str
    cost_items: list[CostItem]
    members: list[MemberOut]
    created_at: datetime
    share_url: str
