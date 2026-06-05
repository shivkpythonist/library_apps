CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    copies_available INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(500),
    membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS borrowings (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    borrowed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    returned_date TIMESTAMP,
    is_returned BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_borrowings_member ON borrowings(member_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_book ON borrowings(book_id);
CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);

-- Insert sample members
INSERT INTO members (name, email, phone, address, is_active)
VALUES 
  ('Shiv Kumar', 'shiv@example.com', '+91-9800000000', '123 Tech Street, Bangalore', true),
  ('Amit Singh', 'amit@example.com', '+91-987000', '456 Code Avenue, Delhi', true)
ON CONFLICT (email) DO NOTHING;

-- Insert sample IT books
INSERT INTO books (title, author, isbn, copies_available)
VALUES 
  ('Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '978-0132350884', 3),
  ('Design Patterns: Elements of Reusable Object-Oriented Software', 'Gang of Four', '978-0201633610', 2),
  ('The Pragmatic Programmer: Your Journey to Mastery', 'David Thomas & Andrew Hunt', '978-0201616224', 4),
  ('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 2),
  ('Refactoring: Improving the Design of Existing Code', 'Martin Fowler', '978-0201485677', 3),
  ('Database Design Manual', 'Lightstone, Teorey & Nadeau', '978-1590590191', 2),
  ('Web Development with Node and Express', 'Ethan Brown', '978-1492053507', 3)
ON CONFLICT (isbn) DO NOTHING;

-- Insert sample borrowing records
INSERT INTO borrowings (member_id, book_id, due_date, is_returned)
SELECT m.id, b.id, CURRENT_DATE + INTERVAL '14 days', false
FROM members m
CROSS JOIN books b
WHERE m.email = 'shiv@example.com' AND b.title = 'Clean Code: A Handbook of Agile Software Craftsmanship'
UNION ALL
SELECT m.id, b.id, CURRENT_DATE + INTERVAL '14 days', false
FROM members m
CROSS JOIN books b
WHERE m.email = 'amit@example.com' AND b.title = 'Design Patterns: Elements of Reusable Object-Oriented Software'
ON CONFLICT DO NOTHING;
