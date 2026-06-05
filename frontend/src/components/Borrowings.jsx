import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function Borrowings() {
  const [borrowings, setBorrowings] = useState([])
  const [books, setBooks] = useState([])
  const [members, setMembers] = useState([])
  const [formData, setFormData] = useState({
    member_id: '', book_id: '', due_date: ''
  })

  useEffect(() => {
    fetchBorrowings()
    fetchBooks()
    fetchMembers()
  }, [])

  const fetchBorrowings = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/borrowings/`)
      setBorrowings(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const fetchBooks = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/books/`)
      setBooks(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const fetchMembers = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/members/`)
      setMembers(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await axios.post(`${API_URL}/api/borrowings/`, {
        member_id: parseInt(formData.member_id),
        book_id: parseInt(formData.book_id),
        due_date: formData.due_date + 'T00:00:00'
      })
      setFormData({ member_id: '', book_id: '', due_date: '' })
      fetchBorrowings()
      fetchBooks()
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleReturn = async (id) => {
    try {
      await axios.post(`${API_URL}/api/borrowings/${id}/return`)
      fetchBorrowings()
      fetchBooks()
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const activeBorrowings = borrowings.filter(b => !b.is_returned)
  const getMemberName = (id) => members.find(m => m.id === id)?.name || 'Unknown'
  const getBookTitle = (id) => books.find(b => b.id === id)?.title || 'Unknown'

  return (
    <div className="section">
      <h2>Borrowings</h2>
      <form onSubmit={handleSubmit} className="form">
        <select value={formData.member_id} onChange={(e) => setFormData({...formData, member_id: e.target.value})} required>
          <option value="">Select Member</option>
          {members.map(m => (<option key={m.id} value={m.id}>{m.name}</option>))}
        </select>
        <select value={formData.book_id} onChange={(e) => setFormData({...formData, book_id: e.target.value})} required>
          <option value="">Select Book</option>
          {books.filter(b => b.copies_available > 0).map(b => (<option key={b.id} value={b.id}>{b.title}</option>))}
        </select>
        <input type="date" value={formData.due_date} onChange={(e) => setFormData({...formData, due_date: e.target.value})} required />
        <button type="submit">Record Borrow</button>
      </form>

      <table className="table">
        <thead>
          <tr><th>Member</th><th>Book</th><th>Borrowed</th><th>Due</th><th>Action</th></tr>
        </thead>
        <tbody>
          {activeBorrowings.map(b => (
            <tr key={b.id}>
              <td>{getMemberName(b.member_id)}</td>
              <td>{getBookTitle(b.book_id)}</td>
              <td>{new Date(b.borrowed_date).toLocaleDateString()}</td>
              <td>{new Date(b.due_date).toLocaleDateString()}</td>
              <td><button onClick={() => handleReturn(b.id)}>Return</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
