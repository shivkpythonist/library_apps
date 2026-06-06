"""Test cases for Books API endpoints."""

import pytest
from fastapi import status


def test_get_books_empty(client):
    """Test getting books when database is empty."""
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_book(client):
    """Test creating a new book."""
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "copies_available": 3
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert data["copies_available"] == book_data["copies_available"]
    assert "id" in data


def test_create_book_duplicate_isbn(client):
    """Test creating a book with duplicate ISBN fails."""
    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "copies_available": 3
    }
    # First book creation should succeed
    response1 = client.post("/books/", json=book_data)
    assert response1.status_code == status.HTTP_200_OK
    
    # Second book with same ISBN should fail
    response2 = client.post("/books/", json=book_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST


def test_get_book_by_id(client, sample_book):
    """Test getting a specific book by ID."""
    response = client.get(f"/books/{sample_book.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_book.id
    assert data["title"] == sample_book.title
    assert data["author"] == sample_book.author


def test_get_book_not_found(client):
    """Test getting a non-existent book."""
    response = client.get("/books/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_book(client, sample_book):
    """Test updating a book."""
    update_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "copies_available": 10
    }
    response = client.put(f"/books/{sample_book.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["author"] == update_data["author"]
    assert data["copies_available"] == update_data["copies_available"]


def test_delete_book(client, sample_book):
    """Test deleting a book."""
    response = client.delete(f"/books/{sample_book.id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify book is deleted
    response = client.get(f"/books/{sample_book.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_books(client, sample_book):
    """Test getting all books."""
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_book.id
