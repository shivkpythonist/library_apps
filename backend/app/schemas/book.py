from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies_available: int = 1
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) < 3:
            raise ValueError('Title must be at least 3 characters long')
        if len(v) > 255:
            raise ValueError('Title must not exceed 255 characters')
        return v.strip()
    
    @field_validator('author')
    @classmethod
    def author_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Author cannot be empty')
        if len(v) < 2:
            raise ValueError('Author must be at least 2 characters long')
        if len(v) > 255:
            raise ValueError('Author must not exceed 255 characters')
        return v.strip()
    
    @field_validator('isbn')
    @classmethod
    def isbn_valid(cls, v):
        clean_isbn = v.replace('-', '').replace(' ', '')
        if not clean_isbn.isdigit():
            raise ValueError('ISBN must contain only digits and hyphens')
        if len(clean_isbn) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        return v.strip()
    
    @field_validator('copies_available')
    @classmethod
    def copies_positive(cls, v):
        if v < 1:
            raise ValueError('Copies available must be at least 1')
        if v > 1000:
            raise ValueError('Copies available cannot exceed 1000')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    copies_available: Optional[int] = None
    
    @field_validator('title')
    @classmethod
    def title_valid(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Title cannot be empty')
            if len(v) < 3:
                raise ValueError('Title must be at least 3 characters long')
            if len(v) > 255:
                raise ValueError('Title must not exceed 255 characters')
        return v
    
    @field_validator('author')
    @classmethod
    def author_valid(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Author cannot be empty')
            if len(v) < 2:
                raise ValueError('Author must be at least 2 characters long')
            if len(v) > 255:
                raise ValueError('Author must not exceed 255 characters')
        return v
    
    @field_validator('copies_available')
    @classmethod
    def copies_valid(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError('Copies available cannot be negative')
            if v > 1000:
                raise ValueError('Copies available cannot exceed 1000')
        return v

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies_available: int
    created_at: datetime
    
    class Config:
        from_attributes = True
