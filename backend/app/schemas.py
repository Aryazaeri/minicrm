from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import PipelineStage

# --- Auth ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Contact ---
class ContactCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class ContactOut(ContactCreate):
    id: int
    created_at: datetime
    class Config: from_attributes = True

# --- Lead ---
class LeadCreate(BaseModel):
    title: str
    value: Optional[float] = 0.0
    stage: Optional[PipelineStage] = PipelineStage.new
    notes: Optional[str] = None
    contact_id: Optional[int] = None

class LeadUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[PipelineStage] = None
    notes: Optional[str] = None
    contact_id: Optional[int] = None

class LeadOut(BaseModel):
    id: int
    title: str
    value: float
    stage: PipelineStage
    notes: Optional[str]
    contact_id: Optional[int]
    created_at: datetime
    class Config: from_attributes = True

# --- Dashboard ---
class DashboardStats(BaseModel):
    total_leads: int
    total_value: float
    won: int
    lost: int
    in_progress: int
