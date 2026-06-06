# API Client Examples

This directory contains example scripts showing how to interact with the Neighborhood Library Service API.

## Prerequisites

Ensure the API is running:

```bash
cd library_apps
docker-compose up
```

API will be available at: `http://localhost:8000`

---

## Python Client

### Installation

```bash
pip install requests
```

### Usage

```bash
python python_client.py
```

### What it demonstrates:

- Creating books with validation
- Creating members with email validation
- Creating borrowing records with date validation
- Listing and filtering borrowings
- Error handling for invalid inputs
- Complete CRUD operations

### Code Example

```python
from datetime import datetime, timedelta
from python_client import LibraryClient

client = LibraryClient()

# Create a book
book = client.create_book(
    title="Clean Code",
    author="Robert C. Martin",
    isbn="978-0132350884",
    copies_available=3
)

# Create a member
member = client.create_member(
    name="John Doe",
    email="john@example.com",
    phone="+1-555-0101"
)

# Create borrowing
due_date = datetime.utcnow() + timedelta(days=14)
borrowing = client.create_borrowing(
    member_id=member['id'],
    book_id=book['id'],
    due_date=due_date
)

# List member's borrowings
borrowings = client.get_member_borrowings(member['id'], active_only=True)
```

---

## cURL Examples

### Prerequisites

- `curl` installed (pre-installed on macOS/Linux)
- Optional: `jq` for formatted JSON output


### Usage

```bash
chmod +x curl_examples.sh
./curl_examples.sh
```

The script will demonstrate:
- All CRUD operations
- Validation error handling
- Query parameter filtering
- Request/response formats

### Manual cURL Commands

**Create a Book:**
```bash
curl -X POST "http://localhost:8000/api/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3
  }' | jq '.'
```

**List Books:**
```bash
curl -X GET "http://localhost:8000/api/books/" | jq '.'
```

**Create Member:**
```bash
curl -X POST "http://localhost:8000/api/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0101"
  }' | jq '.'
```

**Create Borrowing:**
```bash
DUE_DATE=$(date -u -d '+14 days' +%Y-%m-%dT%H:%M:%S)
curl -X POST "http://localhost:8000/api/borrowings/" \
  -H "Content-Type: application/json" \
  -d "{
    \"member_id\": 1,
    \"book_id\": 1,
    \"due_date\": \"$DUE_DATE\"
  }" | jq '.'
```

**Get Active Borrowings:**
```bash
curl -X GET "http://localhost:8000/api/borrowings/?active_only=true" | jq '.'
```

**Return a Book:**
```bash
curl -X POST "http://localhost:8000/api/borrowings/1/return" | jq '.'
```

---

## Interactive API Testing

Use the built-in Swagger UI:

1. Start the API: `docker-compose up`
2. Open browser: http://localhost:8000/docs
3. Try all endpoints directly in the UI

---

## Validation Examples

### Book Validation

Valid book:
```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "copies_available": 3
}
```

Invalid examples:
```json
// Title too short
{"title": "A", "author": "Author", "isbn": "978-0132350884"}

// Invalid ISBN length
{"title": "Book", "author": "Author", "isbn": "12345"}

// Copies out of range
{"title": "Book", "author": "Author", "isbn": "978-0132350884", "copies_available": 2000}
```

### Member Validation

Valid member:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0101",
  "address": "123 Main St"
}
```

Invalid examples:
```json
// Name too short
{"name": "J", "email": "john@example.com"}

// Invalid email
{"name": "John Doe", "email": "invalid-email"}

// Invalid phone format
{"name": "John Doe", "email": "john@example.com", "phone": "abc"}
```

### Borrowing Validation

Valid borrowing:
```json
{
  "member_id": 1,
  "book_id": 1,
  "due_date": "2026-06-20T10:30:00"
}
```

Invalid examples:
```json
// Past due date
{"member_id": 1, "book_id": 1, "due_date": "2026-06-01T10:30:00"}

// Due date too far in future
{"member_id": 1, "book_id": 1, "due_date": "2027-12-31T10:30:00"}

// Member doesn't exist
{"member_id": 99999, "book_id": 1, "due_date": "2026-06-20T10:30:00"}
```

---

## Error Handling

All examples include error handling:

### Python
```python
try:
    book = client.create_book(title="AB", author="Author", isbn="123")
except Exception as e:
    print(f"Error: {e}")
```

### cURL
Check HTTP status code and parse JSON response:
```bash
response=$(curl -s -w "\n%{http_code}" -X POST ...)
status_code=$(echo "$response" | tail -1)
body=$(echo "$response" | head -1)

if [ "$status_code" != "200" ]; then
  echo "Error: $body"
fi
```

---

## Testing All Features

To test all API features end-to-end:

```bash
# 1. Start API
docker-compose up

# 2. In another terminal, run Python client
python python_client.py

# 3. Or run cURL examples
./curl_examples.sh

# 4. View results in Swagger UI
# http://localhost:8000/docs

# 5. Check backend logs
docker-compose logs backend
```

---

## Common Issues

### Connection Refused
API not running. Start with: `docker-compose up`

### Validation Errors
Check error message and refer to [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) for validation rules.

### Email Already Exists
Member with that email already created. Use different email or update existing member.

### Book Not Available
Book has 0 copies. Check `copies_available` or add more copies with update endpoint.

### Member Already Has Active Borrowing
Member cannot borrow multiple copies of same book. Return first copy or update business logic.

