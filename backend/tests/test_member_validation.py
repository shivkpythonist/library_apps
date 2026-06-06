"""Test cases for Members API validation."""

import pytest
from fastapi import status


def test_create_member_invalid_name_empty(client):
    """Test creating member with empty name."""
    member_data = {
        "name": "",
        "email": "test@example.com",
        "phone": "+1-555-0101"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_member_invalid_name_too_short(client):
    """Test creating member with name too short."""
    member_data = {
        "name": "J",
        "email": "test@example.com"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_member_invalid_email_format(client):
    """Test creating member with invalid email."""
    member_data = {
        "name": "Test User",
        "email": "invalid-email",
        "phone": "+1-555-0101"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_member_invalid_phone_too_short(client):
    """Test creating member with phone too short."""
    member_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "123"  # Too short
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_member_invalid_phone_invalid_chars(client):
    """Test creating member with phone containing invalid characters."""
    member_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "555-CALL"  # Invalid characters
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_member_valid_phone_formats(client):
    """Test creating member with valid phone formats."""
    valid_phones = [
        "+1-555-0101",
        "(555) 0101",
        "+1 555 0101",
        "555-0101-1234",
    ]
    
    for phone in valid_phones:
        member_data = {
            "name": f"Test User {phone}",
            "email": f"test{phone.replace('-', '').replace(' ', '')}@example.com",
            "phone": phone
        }
        response = client.post("/members/", json=member_data)
        assert response.status_code == status.HTTP_200_OK, f"Valid phone format failed: {phone}"


def test_create_member_valid_minimal(client):
    """Test creating member with minimal valid data."""
    member_data = {
        "name": "Test User",
        "email": "minimal@example.com"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "minimal@example.com"


def test_create_member_valid_full(client):
    """Test creating member with all fields."""
    member_data = {
        "name": "Test User",
        "email": "full@example.com",
        "phone": "+1-555-0101",
        "address": "123 Main St, City, State"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_200_OK
