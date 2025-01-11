# Sword Fighting Championship Management System

A comprehensive management system for the Sword Fighting Championship league using modern tech stack:
- Backend: FastAPI
- Database: SurrealDB
- Frontend: React

## Project Structure
```
game_of_thrones/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Core configurations
│   │   ├── models/   # Database models
│   │   └── schemas/  # Pydantic schemas
│   └── main.py       # FastAPI application
├── frontend/         # React frontend
└── database/        # SurrealDB related files
```

## Setup Instructions

### Backend Setup
1. Install dependencies:
```bash
uv venv
uv pip install -r requirements.txt
```

2. Start the backend server:
```bash
uvicorn backend.main:app --reload
```

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

### Database Setup
1. Install SurrealDB
2. Configure the database connection in `.env` file
3. Start SurrealDB server
