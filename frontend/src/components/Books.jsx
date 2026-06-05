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
    try {
      if (isEditing) {
        await axios.put(`${API_URL}/api/books/${editingId}`, formData)
        setIsEditing(false)
        setEditingId(null)
      } else {
        await axios.post(`${API_URL}/api/books/`, formData)
      }
      setFormData({ title: '', author: '', isbn: '', copies_available: 1 })
      fetchBooks()
    } catch (error) {
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
      <form onSubmit={handleSubmit} className="form">
        <input
          placeholder="Title"
          value={formData.title}
          onChange={(e) => setFormData({...formData, title: e.target.value})}
          required
        />
        <input
          placeholder="Author"
          value={formData.author}
          onChange={(e) => setFormData({...formData, author: e.target.value})}
          required
        />
        <input
          placeholder="ISBN"
          value={formData.isbn}
          onChange={(e) => setFormData({...formData, isbn: e.target.value})}
          required
        />
        <input
          type="number"
          placeholder="Copies"
          value={formData.copies_available}
          onChange={(e) => setFormData({...formData, copies_available: parseInt(e.target.value)})}
          min="1"
        />
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
