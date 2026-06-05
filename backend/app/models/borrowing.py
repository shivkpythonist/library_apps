from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Borrowing(Base):
    __tablename__ = "borrowings"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    borrowed_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    returned_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    
    member = relationship("Member", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
    
    def __repr__(self):
        return f"<Borrowing(id={self.id}, member_id={self.member_id}, book_id={self.book_id})>"
