#!/usr/bin/env python3
"""
Python client script for Neighborhood Library Service API

This script demonstrates how to interact with the Library Management System API
using Python requests library.

Installation:
    pip install requests

Usage:
    python python_client.py
"""

import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}


class LibraryClient:
    """Client for interacting with the Neighborhood Library Service API"""
    
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.headers = HEADERS
    
    # ===== BOOKS ENDPOINTS =====
    
    def create_book(self, title, author, isbn, copies_available=1):
        """Create a new book"""
        data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "copies_available": copies_available
        }
        response = requests.post(f"{self.base_url}/books/", json=data, headers=self.headers)
        return response.json() if response.status_code == 200 else response.text
    
    def list_books(self):
        """Get all books"""
        response = requests.get(f"{self.base_url}/books/", headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_book(self, book_id):
        """Get a specific book by ID"""
        response = requests.get(f"{self.base_url}/books/{book_id}", headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def update_book(self, book_id, title=None, author=None, copies_available=None):
        """Update a book"""
        data = {}
        if title:
            data["title"] = title
        if author:
            data["author"] = author
        if copies_available is not None:
            data["copies_available"] = copies_available
        
        response = requests.put(f"{self.base_url}/books/{book_id}", json=data, headers=self.headers)
        return response.json() if response.status_code == 200 else response.text
    
    def delete_book(self, book_id):
        """Delete a book"""
        response = requests.delete(f"{self.base_url}/books/{book_id}", headers=self.headers)
        return response.status_code == 200
    
    # ===== MEMBERS ENDPOINTS =====
    
    def create_member(self, name, email, phone=None, address=None):
        """Create a new member"""
        data = {
            "name": name,
            "email": email
        }
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
        
        response = requests.post(f"{self.base_url}/members/", json=data, headers=self.headers)
        return response.json() if response.status_code == 200 else response.text
    
    def list_members(self):
        """Get all members"""
        response = requests.get(f"{self.base_url}/members/", headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_member(self, member_id):
        """Get a specific member by ID"""
        response = requests.get(f"{self.base_url}/members/{member_id}", headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def update_member(self, member_id, name=None, email=None, phone=None, address=None, is_active=None):
        """Update a member"""
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
        if is_active is not None:
            data["is_active"] = is_active
        
        response = requests.put(f"{self.base_url}/members/{member_id}", json=data, headers=self.headers)
        return response.json() if response.status_code == 200 else response.text
    
    # ===== BORROWINGS ENDPOINTS =====
    
    def create_borrowing(self, member_id, book_id, due_date):
        """Create a new borrowing record"""
        data = {
            "member_id": member_id,
            "book_id": book_id,
            "due_date": due_date.isoformat() if isinstance(due_date, datetime) else due_date
        }
        response = requests.post(f"{self.base_url}/borrowings/", json=data, headers=self.headers)
        return response.json() if response.status_code in [200, 201] else response.text
    
    def list_borrowings(self, member_id=None, active_only=False, returned_only=False):
        """List borrowings with optional filters"""
        params = {}
        if member_id:
            params["member_id"] = member_id
        if active_only:
            params["active_only"] = "true"
        if returned_only:
            params["returned_only"] = "true"
        
        response = requests.get(f"{self.base_url}/borrowings/", params=params, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_member_borrowings(self, member_id, active_only=True):
        """Get borrowings for a specific member"""
        params = {"active_only": "true" if active_only else "false"}
        response = requests.get(f"{self.base_url}/borrowings/member/{member_id}", params=params, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def return_book(self, borrowing_id):
        """Return a borrowed book"""
        response = requests.post(f"{self.base_url}/borrowings/{borrowing_id}/return", headers=self.headers)
        return response.json() if response.status_code == 200 else response.text


# ===== EXAMPLE USAGE =====

def main():
    """Demonstrate API usage with examples"""
    
    client = LibraryClient()
    
    print("=" * 60)
    print("Neighborhood Library Service - API Client Demo")
    print("=" * 60)
    
    # 1. Create books
    print("\n1. Creating books...")
    book1 = client.create_book(
        title="Clean Code: A Handbook of Agile Software Craftsmanship",
        author="Robert C. Martin",
        isbn="978-0132350884",
        copies_available=3
    )
    print(f"   Created book: {book1.get('title', 'Error')}")
    
    book2 = client.create_book(
        title="Design Patterns",
        author="Gang of Four",
        isbn="978-0201633610",
        copies_available=2
    )
    print(f"   Created book: {book2.get('title', 'Error')}")
    
    # 2. Create members
    print("\n2. Creating members...")
    member1 = client.create_member(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1-555-0101",
        address="123 Main St, City, State"
    )
    print(f"   Created member: {member1.get('name', 'Error')}")
    
    member2 = client.create_member(
        name="Jane Smith",
        email="jane.smith@example.com",
        phone="+1-555-0102",
        address="456 Oak Ave, City, State"
    )
    print(f"   Created member: {member2.get('name', 'Error')}")
    
    # 3. List all books
    print("\n3. Listing all books...")
    books = client.list_books()
    for book in books:
        print(f"   - {book['title']} by {book['author']} (ISBN: {book['isbn']}, Copies: {book['copies_available']})")
    
    # 4. List all members
    print("\n4. Listing all members...")
    members = client.list_members()
    for member in members:
        print(f"   - {member['name']} ({member['email']}, Active: {member['is_active']})")
    
    # 5. Create borrowing records
    print("\n5. Creating borrowing records...")
    if book1.get('id') and member1.get('id'):
        due_date = datetime.utcnow() + timedelta(days=14)
        borrowing1 = client.create_borrowing(
            member_id=member1['id'],
            book_id=book1['id'],
            due_date=due_date
        )
        print(f"   Borrowing created: {borrowing1.get('id', 'Error')}")
    
    if book2.get('id') and member2.get('id'):
        due_date = datetime.utcnow() + timedelta(days=14)
        borrowing2 = client.create_borrowing(
            member_id=member2['id'],
            book_id=book2['id'],
            due_date=due_date
        )
        print(f"   Borrowing created: {borrowing2.get('id', 'Error')}")
    
    # 6. Get active borrowings for a member
    print(f"\n6. Active borrowings for {member1.get('name', 'member')}...")
    active_borrowings = client.get_member_borrowings(member1['id'], active_only=True)
    for borrowing in active_borrowings:
        print(f"   - Book ID: {borrowing['book_id']}, Due: {borrowing['due_date']}")
    
    # 7. Error handling - Try invalid inputs
    print("\n7. Testing validation (invalid inputs)...")
    print("   Attempting to create book with invalid ISBN...")
    result = client.create_book(
        title="Test Book",
        author="Test Author",
        isbn="invalid",  # Invalid ISBN
        copies_available=1
    )
    if isinstance(result, dict) and 'detail' in result:
        print(f"   ✓ Validation error caught: {result['detail']}")
    else:
        print(f"   Result: {result}")
    
    print("   Attempting to create member with invalid email...")
    result = client.create_member(
        name="Test User",
        email="invalid-email",  # Invalid email
    )
    if isinstance(result, dict) and 'detail' in result:
        print(f"   ✓ Validation error caught: {result['detail']}")
    else:
        print(f"   Result: {result}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
