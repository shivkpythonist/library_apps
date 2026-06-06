import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function Books() {
  const [books, setBooks] = useState([])
  const [formData, setFormData] = useState({
    title: '', author: '', isbn: '', copies_available: 1
  })
  const [isEditing, setIsEditing] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [formErrors, setFormErrors] = useState({})

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/books/`)
      setBooks(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccessMessage('')
    setFormErrors({})
    
    // Validation
    const errors = {}
    if (!formData.title || formData.title.length < 3) {
      errors.title = 'Title must be at least 3 characters'
    }
    if (formData.title && formData.title.length > 255) {
      errors.title = 'Title must not exceed 255 characters'
    }
    if (!formData.author || formData.author.length < 2) {
      errors.author = 'Author must be at least 2 characters'
    }
    if (formData.author && formData.author.length > 255) {
      errors.author = 'Author must not exceed 255 characters'
    }
    const cleanISBN = formData.isbn.replace('-', '').replace(' ', '')
    if (!cleanISBN.match(/^\d{10}$|^\d{13}$/)) {
      errors.isbn = 'ISBN must be 10 or 13 digits'
    }
    if (formData.copies_available < 1 || formData.copies_available > 1000) {
      errors.copies_available = 'Copies must be between 1 and 1000'
    }
    
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors)
      return
    }
    
    try {
      if (isEditing) {
        await axios.put(`${API_URL}/api/books/${editingId}`, formData)
        setSuccessMessage('Book updated successfully!')
        setIsEditing(false)
        setEditingId(null)
      } else {
        await axios.post(`${API_URL}/api/books/`, formData)
        setSuccessMessage('Book added successfully!')
      }
      setTimeout(() => setSuccessMessage(''), 3000)
      setFormData({ title: '', author: '', isbn: '', copies_available: 1 })
      fetchBooks()
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error processing book'
      setError(errorMessage)
      console.error('Error:', error)
    }
  }

  const handleEdit = (book) => {
    setFormData(book)
    setEditingId(book.id)
    setIsEditing(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await axios.delete(`${API_URL}/api/books/${id}`)
        fetchBooks()
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }

  return (
    <div className="section">
      <h2>Books</h2>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}
      <form onSubmit={handleSubmit} className="form">
        <div>
          <input
            placeholder="Title"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className={formErrors.title ? 'input-error' : ''}
            required
          />
          {formErrors.title && <span className="field-error">{formErrors.title}</span>}
        </div>
        <div>
          <input
            placeholder="Author"
            value={formData.author}
            onChange={(e) => setFormData({...formData, author: e.target.value})}
            className={formErrors.author ? 'input-error' : ''}
            required
          />
          {formErrors.author && <span className="field-error">{formErrors.author}</span>}
        </div>
        <div>
          <input
            placeholder="ISBN (10 or 13 digits)"
            value={formData.isbn}
            onChange={(e) => setFormData({...formData, isbn: e.target.value})}
            className={formErrors.isbn ? 'input-error' : ''}
            required
          />
          {formErrors.isbn && <span className="field-error">{formErrors.isbn}</span>}
        </div>
        <div>
          <input
            type="number"
            placeholder="Copies"
            value={formData.copies_available}
            onChange={(e) => setFormData({...formData, copies_available: parseInt(e.target.value)})}
            className={formErrors.copies_available ? 'input-error' : ''}
            min="1"
            max="1000"
          />
          {formErrors.copies_available && <span className="field-error">{formErrors.copies_available}</span>}
        </div>
        <button type="submit">{isEditing ? 'Update' : 'Add'} Book</button>
      </form>

      <table className="table">
        <thead>
          <tr>
            <th>Title</th><th>Author</th><th>ISBN</th><th>Copies</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.map(book => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.isbn}</td>
              <td>{book.copies_available}</td>
              <td>
                <button onClick={() => handleEdit(book)}>Edit</button>
                <button onClick={() => handleDelete(book.id)} className="delete">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
