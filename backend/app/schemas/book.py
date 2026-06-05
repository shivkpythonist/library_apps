from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies_available: int = 1

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    copies_available: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies_available: int
    created_at: datetime
    
    class Config:
        from_attributes = True
