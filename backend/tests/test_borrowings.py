"""Test cases for Borrowings API endpoints."""

import pytest
from datetime import datetime, timedelta
from fastapi import status


def test_get_borrowings_empty(client):
    """Test getting borrowings when database is empty."""
    response = client.get("/borrowings/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_borrowing(client, sample_member, sample_book):
    """Test creating a new borrowing."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["member_id"] == sample_member.id
    assert data["book_id"] == sample_book.id
    assert data["is_returned"] is False
    assert "id" in data


def test_create_borrowing_invalid_member(client, sample_book):
    """Test creating a borrowing with invalid member ID."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": 99999,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_borrowing_invalid_book(client, sample_member):
    """Test creating a borrowing with invalid book ID."""
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": 99999,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_borrowing_by_id(client, sample_borrowing):
    """Test getting a specific borrowing by ID."""
    response = client.get(f"/borrowings/{sample_borrowing.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_borrowing.id
    assert data["member_id"] == sample_borrowing.member_id
    assert data["book_id"] == sample_borrowing.book_id


def test_get_borrowing_not_found(client):
    """Test getting a non-existent borrowing."""
    response = client.get("/borrowings/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_return_book(client, sample_borrowing):
    """Test returning a borrowed book."""
    assert sample_borrowing.is_returned is False
    
    response = client.put(f"/borrowings/{sample_borrowing.id}/return")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_returned"] is True
    assert data["returned_date"] is not None


def test_get_all_borrowings(client, sample_borrowing):
    """Test getting all borrowings."""
    response = client.get("/borrowings/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_borrowing.id


def test_get_active_borrowings(client, sample_borrowing):
    """Test getting only active borrowings."""
    response = client.get("/borrowings/?active_only=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_returned"] is False


def test_get_member_borrowings(client, sample_borrowing):
    """Test getting borrowings for a specific member."""
    response = client.get(f"/borrowings/?member_id={sample_borrowing.member_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["member_id"] == sample_borrowing.member_id


def test_overdue_borrowing(client, sample_member, sample_book):
    """Test creating an overdue borrowing."""
    due_date = (datetime.utcnow() - timedelta(days=5)).isoformat()
    borrowing_data = {
        "member_id": sample_member.id,
        "book_id": sample_book.id,
        "due_date": due_date
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Check if the borrowing was created (API should allow it)
    assert data["member_id"] == sample_member.id
