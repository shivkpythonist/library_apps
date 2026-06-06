#!/bin/bash
# cURL Examples for Neighborhood Library Service API
# 
# This script demonstrates how to interact with the Library Management System API
# using cURL commands.
#
# Prerequisites:
#   - API running at http://localhost:8000
#   - curl installed
#
# Usage:
#   ./curl_examples.sh

API_BASE_URL="http://localhost:8000/api"

echo "=========================================="
echo "Neighborhood Library Service - cURL Examples"
echo "=========================================="

# ===== CREATE BOOK =====
echo ""
echo "1. CREATE A BOOK"
echo "   Command: POST /api/books/"
echo "   Valid example:"
curl -X POST "$API_BASE_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3
  }' | jq '.'

echo ""
echo "   Invalid example (short title):"
curl -X POST "$API_BASE_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AB",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "copies_available": 3
  }' | jq '.'

echo ""
echo "   Invalid example (invalid ISBN):"
curl -X POST "$API_BASE_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "invalid",
    "copies_available": 3
  }' | jq '.'

# ===== LIST ALL BOOKS =====
echo ""
echo "2. LIST ALL BOOKS"
echo "   Command: GET /api/books/"
curl -X GET "$API_BASE_URL/books/" | jq '.'

# ===== GET SPECIFIC BOOK =====
echo ""
echo "3. GET SPECIFIC BOOK"
echo "   Command: GET /api/books/1"
curl -X GET "$API_BASE_URL/books/1" | jq '.'

# ===== CREATE MEMBER =====
echo ""
echo "4. CREATE A MEMBER"
echo "   Command: POST /api/members/"
echo "   Valid example:"
curl -X POST "$API_BASE_URL/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0101",
    "address": "123 Main St, City, State"
  }' | jq '.'

echo ""
echo "   Invalid example (short name):"
curl -X POST "$API_BASE_URL/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J",
    "email": "john@example.com",
    "phone": "+1-555-0101"
  }' | jq '.'

echo ""
echo "   Invalid example (invalid email):"
curl -X POST "$API_BASE_URL/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "invalid-email",
    "phone": "+1-555-0101"
  }' | jq '.'

echo ""
echo "   Invalid example (invalid phone):"
curl -X POST "$API_BASE_URL/members/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "abc"
  }' | jq '.'

# ===== LIST ALL MEMBERS =====
echo ""
echo "5. LIST ALL MEMBERS"
echo "   Command: GET /api/members/"
curl -X GET "$API_BASE_URL/members/" | jq '.'

# ===== CREATE BORROWING =====
echo ""
echo "6. CREATE A BORROWING"
echo "   Command: POST /api/borrowings/"
echo "   Valid example (due_date = 14 days from now):"
DUE_DATE=$(date -u -d '+14 days' +%Y-%m-%dT%H:%M:%S)
curl -X POST "$API_BASE_URL/borrowings/" \
  -H "Content-Type: application/json" \
  -d "{
    \"member_id\": 1,
    \"book_id\": 1,
    \"due_date\": \"$DUE_DATE\"
  }" | jq '.'

echo ""
echo "   Invalid example (past due_date):"
PAST_DATE=$(date -u -d '-1 days' +%Y-%m-%dT%H:%M:%S)
curl -X POST "$API_BASE_URL/borrowings/" \
  -H "Content-Type: application/json" \
  -d "{
    \"member_id\": 1,
    \"book_id\": 1,
    \"due_date\": \"$PAST_DATE\"
  }" | jq '.'

echo ""
echo "   Invalid example (invalid member_id):"
DUE_DATE=$(date -u -d '+14 days' +%Y-%m-%dT%H:%M:%S)
curl -X POST "$API_BASE_URL/borrowings/" \
  -H "Content-Type: application/json" \
  -d "{
    \"member_id\": -1,
    \"book_id\": 1,
    \"due_date\": \"$DUE_DATE\"
  }" | jq '.'

# ===== LIST BORROWINGS =====
echo ""
echo "7. LIST BORROWINGS"
echo "   Command: GET /api/borrowings/"
curl -X GET "$API_BASE_URL/borrowings/" | jq '.'

echo ""
echo "   Filter by member (member_id=1):"
curl -X GET "$API_BASE_URL/borrowings/?member_id=1" | jq '.'

echo ""
echo "   Filter active borrowings only:"
curl -X GET "$API_BASE_URL/borrowings/?active_only=true" | jq '.'

echo ""
echo "   Filter returned borrowings only:"
curl -X GET "$API_BASE_URL/borrowings/?returned_only=true" | jq '.'

# ===== RETURN A BOOK =====
echo ""
echo "8. RETURN A BORROWED BOOK"
echo "   Command: POST /api/borrowings/{borrowing_id}/return"
echo "   (Requires an active borrowing record)"
curl -X POST "$API_BASE_URL/borrowings/1/return" | jq '.'

# ===== UPDATE BOOK =====
echo ""
echo "9. UPDATE A BOOK"
echo "   Command: PUT /api/books/{book_id}"
curl -X PUT "$API_BASE_URL/books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "copies_available": 5
  }' | jq '.'

# ===== UPDATE MEMBER =====
echo ""
echo "10. UPDATE A MEMBER"
echo "    Command: PUT /api/members/{member_id}"
curl -X PUT "$API_BASE_URL/members/1" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1-555-9999",
    "is_active": true
  }' | jq '.'

# ===== DELETE A BOOK =====
echo ""
echo "11. DELETE A BOOK"
echo "    Command: DELETE /api/books/{book_id}"
curl -X DELETE "$API_BASE_URL/books/1" | jq '.'

echo ""
echo "=========================================="
echo "Examples complete!"
echo "=========================================="
