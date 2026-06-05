# 📚 Library Management System

A complete library management system with FastAPI backend and Next.js frontend.

## Quick Start

```bash
cd library_apps
docker-compose up
```

Access at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Database Setup

### Automatic (with Docker) ✅
When using `docker-compose up`, the database schema is initialized **automatically**:
- PostgreSQL container starts
- `database/schema.sql` is automatically executed
- All tables and indexes are created
- Backend connects and runs

```bash
docker-compose up
```

### Notes & Troubleshooting

- If you see a warning about `Docker Compose requires buildx plugin to be installed`, ensure you have Docker Desktop installed and up-to-date. On macOS, start Docker Desktop: `open /Applications/Docker.app` and wait for the whale icon to finish initializing.
- If the Postgres data directory already exists the image will skip initialization (message: "Database directory appears to contain a database; Skipping initialization"). To force re-initialize the database remove the volumes and bring the stack down:

```bash
docker-compose down -v
docker-compose up --build
```

- If the frontend build fails due to TypeScript or missing types, I adjusted the project to install dev dependencies during image build. If you still see build issues, run locally to reproduce and fix:

```bash
cd frontend
npm install
npm run build
```

### Manual Database Initialization
If you need to initialize the database separately or run locally:

```bash
# Make sure PostgreSQL is running
# Then run the initialization script:
./init-db.sh
```

**Prerequisites:**
- PostgreSQL running on localhost:5432
- `psql` client installed
- `.env` file with database credentials

The script will:
- Load credentials from `.env` file
- Execute `database/schema.sql`
- Create tables and indexes
- Verify the schema was loaded successfully

## Tech Stack
- Backend: FastAPI, PostgreSQL, SQLAlchemy
- Frontend: React, Next.js, Axios
- Deployment: Docker Compose

## Features
✅ Books management
✅ Members management
✅ Borrowing/Returning system
✅ Inventory tracking
✅ RESTful API with Swagger docs
✅ Modern responsive UI

## Manual Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
