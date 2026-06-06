"""Test cases for Members API endpoints."""

import pytest
from fastapi import status


def test_get_members_empty(client):
    """Test getting members when database is empty."""
    response = client.get("/members/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_member(client):
    """Test creating a new member."""
    member_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900",
        "address": "123 Main St, City",
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == member_data["name"]
    assert data["email"] == member_data["email"]
    assert data["phone"] == member_data["phone"]
    assert data["address"] == member_data["address"]
    assert data["is_active"] is True
    assert "id" in data


def test_create_member_duplicate_email(client):
    """Test creating a member with duplicate email fails."""
    member_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900",
        "address": "123 Main St, City",
    }
    # First member creation should succeed
    response1 = client.post("/members/", json=member_data)
    assert response1.status_code == status.HTTP_200_OK
    
    # Second member with same email should fail
    response2 = client.post("/members/", json=member_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST


def test_get_member_by_id(client, sample_member):
    """Test getting a specific member by ID."""
    response = client.get(f"/members/{sample_member.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sample_member.id
    assert data["name"] == sample_member.name
    assert data["email"] == sample_member.email


def test_get_member_not_found(client):
    """Test getting a non-existent member."""
    response = client.get("/members/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_member(client, sample_member):
    """Test updating a member."""
    update_data = {
        "name": "Updated Name",
        "phone": "+1-999-999-9999",
        "is_active": False
    }
    response = client.put(f"/members/{sample_member.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["phone"] == update_data["phone"]
    assert data["is_active"] == update_data["is_active"]


def test_deactivate_member(client, sample_member):
    """Test deactivating a member."""
    response = client.put(f"/members/{sample_member.id}", json={"is_active": False})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_active"] is False


def test_get_all_members(client, sample_member):
    """Test getting all members."""
    response = client.get("/members/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_member.id
    assert data[0]["name"] == sample_member.name
