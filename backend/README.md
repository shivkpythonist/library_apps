# Neighborhood Library Service - Backend API

## Overview
REST API server built with FastAPI and PostgreSQL.

## Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run server**
   ```bash
   uvicorn app.main:app --reload
   ```

Access at: http://localhost:8000
Docs: http://localhost:8000/docs
