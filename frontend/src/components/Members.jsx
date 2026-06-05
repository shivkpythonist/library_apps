import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function Members() {
  const [members, setMembers] = useState([])
  const [formData, setFormData] = useState({
    name: '', email: '', phone: '', address: ''
  })
  const [isEditing, setIsEditing] = useState(false)
  const [editingId, setEditingId] = useState(null)

  useEffect(() => {
    fetchMembers()
  }, [])

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
      if (isEditing) {
        await axios.put(`${API_URL}/api/members/${editingId}`, formData)
        setIsEditing(false)
        setEditingId(null)
      } else {
        await axios.post(`${API_URL}/api/members/`, formData)
      }
      setFormData({ name: '', email: '', phone: '', address: '' })
      fetchMembers()
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleEdit = (member) => {
    setFormData(member)
    setEditingId(member.id)
    setIsEditing(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await axios.delete(`${API_URL}/api/members/${id}`)
        fetchMembers()
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }

  return (
    <div className="section">
      <h2>Members</h2>
      <form onSubmit={handleSubmit} className="form">
        <input placeholder="Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required />
        <input placeholder="Email" type="email" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} required />
        <input placeholder="Phone" value={formData.phone} onChange={(e) => setFormData({...formData, phone: e.target.value})} />
        <input placeholder="Address" value={formData.address} onChange={(e) => setFormData({...formData, address: e.target.value})} />
        <button type="submit">{isEditing ? 'Update' : 'Add'} Member</button>
      </form>

      <table className="table">
        <thead>
          <tr><th>Name</th><th>Email</th><th>Phone</th><th>Address</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {members.map(member => (
            <tr key={member.id}>
              <td>{member.name}</td>
              <td>{member.email}</td>
              <td>{member.phone}</td>
              <td>{member.address}</td>
              <td>
                <button onClick={() => handleEdit(member)}>Edit</button>
                <button onClick={() => handleDelete(member.id)} className="delete">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
