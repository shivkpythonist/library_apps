"""Pytest configuration and fixtures for Library Management System tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.book import Book
from app.models.member import Member
from app.models.borrowing import Borrowing


@pytest.fixture(scope="session")
def db_engine():
    """Create an in-memory SQLite database for tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with overridden database dependency."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_member(db_session):
    """Create a sample member for testing."""
    member = Member(
        name="Test User",
        email="test@example.com",
        phone="+1-234-567-8900",
        address="123 Test St, Test City",
        is_active=True
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)
    return member


@pytest.fixture
def sample_book(db_session):
    """Create a sample book for testing."""
    book = Book(
        title="Test Book",
        author="Test Author",
        isbn="978-0-123456-78-9",
        copies_available=5
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


@pytest.fixture
def sample_borrowing(db_session, sample_member, sample_book):
    """Create a sample borrowing for testing."""
    from datetime import datetime, timedelta
    borrowing = Borrowing(
        member_id=sample_member.id,
        book_id=sample_book.id,
        due_date=datetime.utcnow() + timedelta(days=14),
        is_returned=False
    )
    db_session.add(borrowing)
    db_session.commit()
    db_session.refresh(borrowing)
    return borrowing
