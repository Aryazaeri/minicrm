# Mini CRM

A lightweight CRM built with FastAPI, PostgreSQL, and React. Manage leads through a drag-and-drop Kanban pipeline, track contacts, and monitor your sales dashboard.

## Features
- Drag-and-drop Kanban pipeline (New → Contacted → Negotiating → Won/Lost)
- Lead creation with value and notes
- Contact directory
- Dashboard with pipeline stats and total value
- JWT authentication

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL |
| Frontend | React, Tailwind CSS, Vite |
| Auth | JWT (python-jose, passlib) |
| DevOps | Docker, Docker Compose |

## Quick Start

### With Docker
```bash
docker-compose up --build
```
Backend runs at http://localhost:8000  
Frontend: `cd frontend && npm install && npm run dev` → http://localhost:5173

### Without Docker
```bash
# Backend
cd backend
pip install -r requirements.txt
# Set DATABASE_URL in .env
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## API Docs
Visit http://localhost:8000/docs for the interactive Swagger UI.

## Project Structure
```
MiniCRM/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Config, DB, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/        # Dashboard, Pipeline, Contacts
│       ├── components/   # Layout, shared UI
│       └── api.js        # Axios client
└── docker-compose.yml
```
