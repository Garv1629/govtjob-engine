# GovtJob AI Agent - Production Foundation

GovtJob AI Agent is an automated recruitment monitoring, AI eligibility analysis, and application assistant platform tailored for Indian government job examinations.

---

## 🏛 System Architecture Overview

* **Backend**: Python 3.13 + FastAPI + SQLAlchemy + Pydantic v2 + Alembic + APScheduler
* **Frontend**: Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS
* **Database**: SQLite (Development / MVP) / PostgreSQL (Production ready schema)
* **Automation & AI**: Playwright Headless + OpenAI / Gemini LLM Integration + Python Telegram Bot

---

## 📁 Repository Structure

```
.
├── backend/                  # FastAPI Application Server
│   ├── alembic/              # Database Migrations
│   ├── app/                  # Application Core & Modules
│   │   ├── api/              # Route Handlers & Schemas
│   │   ├── core/             # Configuration, Security, Logging
│   │   ├── db/               # SQLAlchemy Models & Repositories
│   │   ├── modules/          # Scraper, AI, Eligibility, Playwright Skeletons
│   │   └── utils/            # Helper utilities
│   ├── tests/                # Pytest Test Suites
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                 # Next.js 15 Frontend Portal
│   ├── src/
│   │   ├── app/              # App Router Pages (Dashboard, Jobs, Settings)
│   │   ├── components/       # UI Components & Layout
│   │   └── lib/              # API Client & Helpers
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml        # Multi-container Deployment Setup
```

---

## 🚀 Quick Setup & Local Development

### Prerequisites
* Python 3.13+
* Node.js 20+ & npm / pnpm
* Docker & Docker Compose (Optional)

### Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Access API Documentation at: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access Web Dashboard at: `http://localhost:3000`

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```
