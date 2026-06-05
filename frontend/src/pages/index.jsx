import React, { useState } from 'react'
import Dashboard from '../components/Dashboard'
import Books from '../components/Books'
import Members from '../components/Members'
import Borrowings from '../components/Borrowings'

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="container">
      <header>
        <h1>📚 Library Management System</h1>
      </header>

      <nav className="tabs">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''} 
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'books' ? 'active' : ''} 
          onClick={() => setActiveTab('books')}
        >
          Books
        </button>
        <button 
          className={activeTab === 'members' ? 'active' : ''} 
          onClick={() => setActiveTab('members')}
        >
          Members
        </button>
        <button 
          className={activeTab === 'borrowings' ? 'active' : ''} 
          onClick={() => setActiveTab('borrowings')}
        >
          Borrowings
        </button>
      </nav>

      <main>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'books' && <Books />}
        {activeTab === 'members' && <Members />}
        {activeTab === 'borrowings' && <Borrowings />}
      </main>
    </div>
  )
}
