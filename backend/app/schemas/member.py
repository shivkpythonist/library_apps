from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    membership_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
