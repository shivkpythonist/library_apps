"""Test cases for Borrowings API validation."""

import pytest
from datetime import datetime, timedelta
from fastapi import status


def test_create_borrowing_invalid_member_id_negative(client, sample_book):
    """Test creating borrowing with negative member ID."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": -1,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_borrowing_invalid_member_id_zero(client, sample_book):
    """Test creating borrowing with zero member ID."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": 0,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_borrowing_invalid_book_id_negative(client, sample_member):
    """Test creating borrowing with negative book ID."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": -1,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_borrowing_invalid_due_date_past(client, sample_member, sample_book):
    """Test creating borrowing with past due date."""
    due_date = (datetime.utcnow() - timedelta(days=5)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "future" in response.json()["detail"].lower()


def test_create_borrowing_invalid_due_date_current(client, sample_member, sample_book):
    """Test creating borrowing with current time as due date."""
    due_date = datetime.utcnow().isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_borrowing_invalid_due_date_too_far(client, sample_member, sample_book):
    """Test creating borrowing with due date more than 365 days away."""
    due_date = (datetime.utcnow() + timedelta(days=400)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "365" in response.json()["detail"]


def test_create_borrowing_valid_boundary_dates(client, sample_member, sample_book):
    """Test creating borrowing with valid boundary due dates."""
    # Valid: exactly 1 day in future
    due_date_1day = (datetime.utcnow() + timedelta(days=1)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date_1day
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_200_OK
    
    # Valid: exactly 365 days in future
    due_date_365days = (datetime.utcnow() + timedelta(days=365)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date_365days
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_200_OK


def test_create_borrowing_valid_standard_date(client, sample_member, sample_book):
    """Test creating borrowing with standard 14-day due date."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["due_date"] is not None
