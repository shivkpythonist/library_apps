from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
from typing import Optional

class BorrowingCreate(BaseModel):
    member_id: int
    book_id: int
    due_date: datetime
    
    @field_validator('member_id')
    @classmethod
    def member_id_valid(cls, v):
        if v <= 0:
            raise ValueError('Member ID must be a positive integer')
        return v
    
    @field_validator('book_id')
    @classmethod
    def book_id_valid(cls, v):
        if v <= 0:
            raise ValueError('Book ID must be a positive integer')
        return v
    
    @field_validator('due_date')
    @classmethod
    def due_date_valid(cls, v):
        now = datetime.utcnow()
        if v <= now:
            raise ValueError('Due date must be in the future')
        if v > now + timedelta(days=365):
            raise ValueError('Due date cannot be more than 365 days in the future')
        return v

class BorrowingResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime] = None
    is_returned: bool
    
    class Config:
        from_attributes = True
