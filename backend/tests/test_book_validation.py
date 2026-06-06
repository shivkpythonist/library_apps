"""Test cases for Books API validation."""

import pytest
from fastapi import status


def test_create_book_invalid_title_empty(client):
    """Test creating book with empty title."""
    book_data = {
        "title": "",
        "author": "Test Author",
        "isbn": "978-0132350884",
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_invalid_title_too_short(client):
    """Test creating book with title too short."""
    book_data = {
        "title": "AB",
        "author": "Test Author",
        "isbn": "978-0132350884",
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_invalid_author_too_short(client):
    """Test creating book with author too short."""
    book_data = {
        "title": "Test Book",
        "author": "A",
        "isbn": "978-0132350884",
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_invalid_isbn_format(client):
    """Test creating book with invalid ISBN format."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "invalid-isbn",
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "ISBN" in response.json()["detail"]


def test_create_book_invalid_isbn_wrong_length(client):
    """Test creating book with ISBN of wrong length."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "12345",  # Only 5 digits
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_invalid_copies_zero(client):
    """Test creating book with zero copies."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "978-0132350884",
        "copies_available": 0
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_invalid_copies_exceeds_max(client):
    """Test creating book with copies exceeding max."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "978-0132350884",
        "copies_available": 2000
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_book_valid_isbn_10(client):
    """Test creating book with valid 10-digit ISBN."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "0132350882",  # Valid 10-digit
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_200_OK


def test_create_book_valid_isbn_13(client):
    """Test creating book with valid 13-digit ISBN."""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "978-0132350884",  # Valid 13-digit with hyphens
        "copies_available": 1
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_200_OK
