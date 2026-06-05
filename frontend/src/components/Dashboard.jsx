import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalBooks: 0,
    totalMembers: 0,
    activeBorrowings: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const [booksRes, membersRes, borrowingsRes] = await Promise.all([
        axios.get(`${API_URL}/api/books/`),
        axios.get(`${API_URL}/api/members/`),
        axios.get(`${API_URL}/api/borrowings/`)
      ])

      const activeBorrowings = borrowingsRes.data.filter(b => !b.is_returned).length

      setStats({
        totalBooks: booksRes.data.length,
        totalMembers: membersRes.data.length,
        activeBorrowings
      })
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="section"><p>Loading...</p></div>

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Books</h3>
          <p className="stat-number">{stats.totalBooks}</p>
        </div>
        <div className="stat-card">
          <h3>Total Members</h3>
          <p className="stat-number">{stats.totalMembers}</p>
        </div>
        <div className="stat-card">
          <h3>Active Borrowings</h3>
          <p className="stat-number">{stats.activeBorrowings}</p>
        </div>
      </div>
    </div>
  )
}
