from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BorrowingCreate(BaseModel):
    member_id: int
    book_id: int
    due_date: datetime

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
