from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Borrowing, Book, Member
from ..schemas import BorrowingCreate, BorrowingResponse
from ..database import get_db

router = APIRouter(prefix="/api/borrowings", tags=["borrowings"])

@router.post("/", response_model=BorrowingResponse, status_code=status.HTTP_201_CREATED)
def create_borrowing(borrowing: BorrowingCreate, db: Session = Depends(get_db)):
    """Record a book borrowing"""
    # Check if book exists and has copies available
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.copies_available <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not available")
    
    # Check if member exists
    member = db.query(Member).filter(Member.id == borrowing.member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    # Check if member already has an active borrowing of this book
    existing_borrowing = db.query(Borrowing).filter(
        Borrowing.member_id == borrowing.member_id,
        Borrowing.book_id == borrowing.book_id,
        Borrowing.is_returned == False
    ).first()
    if existing_borrowing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already has an active borrowing of this book"
        )
    
    # Create borrowing record
    db_borrowing = Borrowing(**borrowing.dict())
    book.copies_available -= 1
    
    db.add(db_borrowing)
    db.add(book)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

@router.get("/", response_model=list[BorrowingResponse])
def list_borrowings(
    member_id: int = Query(None, description="Filter by member ID"),
    returned_only: bool = Query(False, description="Show only returned books"),
    active_only: bool = Query(False, description="Show only active borrowings"),
    db: Session = Depends(get_db)
):
    """List borrowing records with optional filters"""
    query = db.query(Borrowing)
    
    if member_id:
        query = query.filter(Borrowing.member_id == member_id)
    
    if active_only:
        query = query.filter(Borrowing.is_returned == False)
    elif returned_only:
        query = query.filter(Borrowing.is_returned == True)
    
    return query.all()

@router.get("/member/{member_id}", response_model=list[BorrowingResponse])
def get_member_borrowings(
    member_id: int,
    active_only: bool = Query(True, description="Show only active borrowings"),
    db: Session = Depends(get_db)
):
    """Get borrowings for a specific member"""
    query = db.query(Borrowing).filter(Borrowing.member_id == member_id)
    
    if active_only:
        query = query.filter(Borrowing.is_returned == False)
    
    return query.all()

@router.post("/{borrowing_id}/return", response_model=BorrowingResponse)
def return_book(borrowing_id: int, db: Session = Depends(get_db)):
    """Record book return"""
    borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing record not found")
    
    if borrowing.is_returned:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")
    
    # Update borrowing record
    borrowing.returned_date = datetime.utcnow()
    borrowing.is_returned = True
    
    # Increment book copies
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    book.copies_available += 1
    
    db.add(borrowing)
    db.add(book)
    db.commit()
    db.refresh(borrowing)
    return borrowing
