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
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [selectedMemberId, setSelectedMemberId] = useState('')

  useEffect(() => {
    fetchBorrowings()
    fetchBooks()
    fetchMembers()
  }, [selectedMemberId])

  const fetchBorrowings = async () => {
    try {
      const url = selectedMemberId 
        ? `${API_URL}/api/borrowings/?member_id=${selectedMemberId}`
        : `${API_URL}/api/borrowings/`
      const response = await axios.get(url)
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
    setError('')
    setSuccessMessage('')
    try {
      await axios.post(`${API_URL}/api/borrowings/`, {
        member_id: parseInt(formData.member_id),
        book_id: parseInt(formData.book_id),
        due_date: formData.due_date + 'T00:00:00'
      })
      setFormData({ member_id: '', book_id: '', due_date: '' })
      setSuccessMessage('Book borrowed successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
      fetchBorrowings()
      fetchBooks()
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error recording borrowing'
      setError(errorMessage)
      console.error('Error:', error)
    }
  }

  const handleReturn = async (id) => {
    try {
      setError('')
      await axios.post(`${API_URL}/api/borrowings/${id}/return`)
      setSuccessMessage('Book returned successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
      fetchBorrowings()
      fetchBooks()
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error returning book'
      setError(errorMessage)
      console.error('Error:', error)
    }
  }

  const activeBorrowings = borrowings.filter(b => !b.is_returned)
  const returnedBorrowings = borrowings.filter(b => b.is_returned)
  const getMemberName = (id) => members.find(m => m.id === id)?.name || 'Unknown'
  const getBookTitle = (id) => books.find(b => b.id === id)?.title || 'Unknown'

  return (
    <div className="section">
      <h2>Borrowings</h2>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}
      
      <div className="filter-section">
        <label>Filter by Member:</label>
        <select value={selectedMemberId} onChange={(e) => setSelectedMemberId(e.target.value)}>
          <option value="">All Members</option>
          {members.map(m => (<option key={m.id} value={m.id}>{m.name}</option>))}
        </select>
      </div>

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

      {returnedBorrowings.length > 0 && (
        <div className="returned-section">
          <h3>Returned Books History</h3>
          <table className="table">
            <thead>
              <tr><th>Member</th><th>Book</th><th>Borrowed</th><th>Due</th><th>Returned</th></tr>
            </thead>
            <tbody>
              {returnedBorrowings.map(b => (
                <tr key={b.id} className="returned-row">
                  <td>{getMemberName(b.member_id)}</td>
                  <td>{getBookTitle(b.book_id)}</td>
                  <td>{new Date(b.borrowed_date).toLocaleDateString()}</td>
                  <td>{new Date(b.due_date).toLocaleDateString()}</td>
                  <td>{b.returned_date ? new Date(b.returned_date).toLocaleDateString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
