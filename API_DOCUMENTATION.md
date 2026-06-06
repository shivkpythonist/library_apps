# API Documentation - Neighborhood Library Service

## Overview

The Neighborhood Library Service provides a comprehensive REST API for managing a library system with books, members, and borrowings. This document describes all endpoints, validation rules, and example usage.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication is required. In production, implement JWT or similar mechanisms.

---

## 1. Books Endpoints

### Create Book

**Endpoint:** `POST /books/`

**Request Body:**
```json
{
  "title": "string (3-255 characters)",
  "author": "string (2-255 characters)",
  "isbn": "string (10 or 13 digits, with optional hyphens)",
  "copies_available": "integer (1-1000, default: 1)"
}
```

**Validation Rules:**
- `title`: 
  - Required, cannot be empty
  - Minimum 3 characters, maximum 255 characters
- `author`:
  - Required, cannot be empty
  - Minimum 2 characters, maximum 255 characters
- `isbn`:
  - Required
  - Must be exactly 10 or 13 digits (hyphens and spaces are allowed but removed for validation)
  - Must be unique (cannot have duplicate ISBNs)
- `copies_available`:
  - Optional, defaults to 1
  - Must be positive integer between 1-1000

**Success Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "copies_available": 3,
  "created_at": "2026-06-06T10:30:00"
}
```

**Error Response:** `422 Unprocessable Entity`
```json
{
  "detail": "Title must be at least 3 characters long"
}
```

### List Books

**Endpoint:** `GET /books/`

**Response:** `200 OK` (array of book objects)
```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3,
    "created_at": "2026-06-06T10:30:00"
  }
]
```

### Get Book by ID

**Endpoint:** `GET /books/{book_id}`

**Response:** `200 OK` (single book object) or `404 Not Found`

### Update Book

**Endpoint:** `PUT /books/{book_id}`

**Request Body:** (all fields optional)
```json
{
  "title": "string",
  "author": "string",
  "copies_available": "integer"
}
```

**Validation Rules:** Same as Create Book (for fields being updated)

### Delete Book

**Endpoint:** `DELETE /books/{book_id}`

**Response:** `200 OK` or `404 Not Found`

---

## 2. Members Endpoints

### Create Member

**Endpoint:** `POST /members/`

**Request Body:**
```json
{
  "name": "string (2-255 characters)",
  "email": "string (valid email format)",
  "phone": "string (7-20 characters, optional)",
  "address": "string (0-500 characters, optional)"
}
```

**Validation Rules:**
- `name`:
  - Required, cannot be empty
  - Minimum 2 characters, maximum 255 characters
- `email`:
  - Required
  - Must be valid email format
  - Must be unique (cannot have duplicate emails)
- `phone`:
  - Optional
  - If provided: 7-20 characters
  - Allowed characters: digits, spaces, hyphens, plus sign, parentheses
  - Example: "+1-555-0101", "(555) 0101", "+1 555 0101"
- `address`:
  - Optional
  - Maximum 500 characters

**Success Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0101",
  "address": "123 Main St, City",
  "membership_date": "2026-06-06T10:30:00",
  "is_active": true
}
```

### List Members

**Endpoint:** `GET /members/`

**Response:** `200 OK` (array of member objects)

### Get Member by ID

**Endpoint:** `GET /members/{member_id}`

**Response:** `200 OK` or `404 Not Found`

### Update Member

**Endpoint:** `PUT /members/{member_id}`

**Request Body:** (all fields optional)
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "is_active": "boolean"
}
```

---

## 3. Borrowings Endpoints

### Create Borrowing

**Endpoint:** `POST /borrowings/`

**Request Body:**
```json
{
  "member_id": "integer",
  "book_id": "integer",
  "due_date": "ISO 8601 datetime string"
}
```

**Validation Rules:**
- `member_id`:
  - Required
  - Must be positive integer > 0
  - Member must exist
- `book_id`:
  - Required
  - Must be positive integer > 0
  - Book must exist
  - Book must have available copies
- `due_date`:
  - Required
  - Must be valid ISO 8601 datetime (e.g., "2026-06-20T10:30:00")
  - Must be in the future (cannot be past or current time)
  - Cannot be more than 365 days in the future
- **Business Rule:**
  - Member cannot borrow multiple copies of the same book
  - Attempting to do so returns `400 Bad Request`: "Member already has an active borrowing of this book"

**Success Response:** `201 Created`
```json
{
  "id": 1,
  "member_id": 1,
  "book_id": 1,
  "borrowed_date": "2026-06-06T10:30:00",
  "due_date": "2026-06-20T10:30:00",
  "returned_date": null,
  "is_returned": false
}
```

**Error Response Examples:**

Invalid member:
```json
{
  "detail": "Member ID must be a positive integer"
}
```

Past due date:
```json
{
  "detail": "Due date must be in the future"
}
```

Duplicate borrowing:
```json
{
  "detail": "Member already has an active borrowing of this book"
}
```

### List Borrowings

**Endpoint:** `GET /borrowings/`

**Query Parameters:**
- `member_id` (optional): Filter by member ID
- `active_only` (optional): Set to "true" to show only active borrowings
- `returned_only` (optional): Set to "true" to show only returned borrowings

**Examples:**
```
GET /borrowings/                           # All borrowings
GET /borrowings/?member_id=1               # All borrowings for member 1
GET /borrowings/?active_only=true          # Only active borrowings
GET /borrowings/?returned_only=true        # Only returned borrowings
GET /borrowings/?member_id=1&active_only=true  # Active borrowings for member 1
```

### Get Member Borrowings

**Endpoint:** `GET /borrowings/member/{member_id}`

**Query Parameters:**
- `active_only` (optional, default: true): Filter by returned status

**Response:** `200 OK` (array of borrowing objects)

### Return Book

**Endpoint:** `POST /borrowings/{borrowing_id}/return`

**Response:** `200 OK`
```json
{
  "id": 1,
  "member_id": 1,
  "book_id": 1,
  "borrowed_date": "2026-06-06T10:30:00",
  "due_date": "2026-06-20T10:30:00",
  "returned_date": "2026-06-10T14:45:00",
  "is_returned": true
}
```

---

## Error Handling

### Common HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Validation error or business logic error
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Invalid request format or validation error
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "detail": "Human-readable error message"
}
```

---

## Client Examples

### Python Example

```python
import requests
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000/api"

# Create a book
book_data = {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3
}
response = requests.post(f"{API_BASE_URL}/books/", json=book_data)
book = response.json()

# Create a member
member_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0101"
}
response = requests.post(f"{API_BASE_URL}/members/", json=member_data)
member = response.json()

# Create a borrowing
due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
borrowing_data = {
    "member_id": member["id"],
    "book_id": book["id"],
    "due_date": due_date
}
response = requests.post(f"{API_BASE_URL}/borrowings/", json=borrowing_data)
borrowing = response.json()

# List active borrowings for member
response = requests.get(
    f"{API_BASE_URL}/borrowings/member/{member['id']}?active_only=true"
)
active_borrowings = response.json()

# Return a book
response = requests.post(f"{API_BASE_URL}/borrowings/{borrowing['id']}/return")
returned_borrowing = response.json()
```

### cURL Example

```bash
# Create a book
curl -X POST "http://localhost:8000/api/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3
  }'

# Create a member
curl -X POST "http://localhost:8000/api/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0101"
  }'

# List active borrowings
curl -X GET "http://localhost:8000/api/borrowings/?active_only=true"

# Return a book
curl -X POST "http://localhost:8000/api/borrowings/1/return"
```

---

## Testing the API

### Using Swagger/OpenAPI UI

Access the interactive API documentation at:
```
http://localhost:8000/docs
```

### Using provided scripts

1. **Python client:**
   ```bash
   python examples/python_client.py
   ```

2. **cURL examples:**
   ```bash
   chmod +x examples/curl_examples.sh
   ./examples/curl_examples.sh
   ```

---

## Rate Limiting

Currently not implemented. Recommended for production use.

## Logging

All API requests and errors are logged. Check Docker container logs:
```bash
docker-compose logs backend
```
