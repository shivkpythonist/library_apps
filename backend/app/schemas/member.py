from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def name_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v) > 255:
            raise ValueError('Name must not exceed 255 characters')
        return v.strip()
    
    @field_validator('phone')
    @classmethod
    def phone_valid(cls, v):
        if v is not None:
            valid_chars = set('0123456789+- ()')
            if not all(c in valid_chars for c in v):
                raise ValueError('Phone number contains invalid characters')
            if len(v) < 7:
                raise ValueError('Phone number must be at least 7 characters')
            if len(v) > 20:
                raise ValueError('Phone number must not exceed 20 characters')
        return v
    
    @field_validator('address')
    @classmethod
    def address_valid(cls, v):
        if v is not None:
            if len(v) > 500:
                raise ValueError('Address must not exceed 500 characters')
        return v

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('name')
    @classmethod
    def name_valid(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Name cannot be empty')
            if len(v) < 2:
                raise ValueError('Name must be at least 2 characters long')
            if len(v) > 255:
                raise ValueError('Name must not exceed 255 characters')
        return v
    
    @field_validator('phone')
    @classmethod
    def phone_valid(cls, v):
        if v is not None:
            valid_chars = set('0123456789+- ()')
            if not all(c in valid_chars for c in v):
                raise ValueError('Phone number contains invalid characters')
            if len(v) < 7:
                raise ValueError('Phone number must be at least 7 characters')
            if len(v) > 20:
                raise ValueError('Phone number must not exceed 20 characters')
        return v
    
    @field_validator('address')
    @classmethod
    def address_valid(cls, v):
        if v is not None:
            if len(v) > 500:
                raise ValueError('Address must not exceed 500 characters')
        return v

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
