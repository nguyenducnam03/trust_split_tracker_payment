from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime

class CostItem(BaseModel):
    name: str
    total: float

class MemberInput(BaseModel):
    name: str
    amount: float

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Member name cannot be empty')
        return v.strip()

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

class CreateSessionRequest(BaseModel):
    name: str
    cost_items: list[CostItem] = []
    members: list[MemberInput]

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Session name cannot be empty')
        return v.strip()

    @field_validator('members')
    @classmethod
    def members_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('At least one member is required')
        names = [m.name.lower() for m in v]
        if len(names) != len(set(names)):
            raise ValueError('Member names must be unique')
        return v

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
