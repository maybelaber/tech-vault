# TechVault — Corporate Knowledge Sharing Platform (Telegram Mini App)

Monorepo: **backend** (FastAPI), **frontend** (Vite + React + Tailwind), **PostgreSQL**.

## Domain (mapping from TZ)

- **Employees / Teams** (was: Students / Groups)
- **Mentors / Tech Leads** (was: Teachers)
- **Technologies** (e.g. Python, Kubernetes, Figma) (was: Subjects)
- **Skill Levels** (Junior, Middle, Senior) (was: Semesters)
- **Docs / Blueprints / Snippets** (was: Cheat Sheets / Labs)

## Tech Stack

- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic
- **DB:** PostgreSQL (schemas: `reference`, `user_data`)
- **Frontend:** React (Vite), Tailwind CSS, shadcn/ui-ready (lucide-react)
- **Infra:** Docker & Docker Compose
- **Auth:** Telegram `initData` validation (to be wired)

## Quick Start

### Docker (recommended)

```bash
cp .env.example .env
docker compose up -d
```

- API: http://localhost:8000 (docs: http://localhost:8000/docs)
- Frontend (placeholder): http://localhost:5173
- Postgres: localhost:5432

### Backend (local)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
# Set DATABASE_URL in .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend (local)

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
backend/
  app/
    api/          # Routes (health, ...)
    core/         # Config, DB session, DI
    models/       # reference.py (technologies, mentors, teams, skill_levels)
                  # core.py (users, resources, ratings)
    repositories/
    services/
  alembic/
frontend/
  src/
    pages/        # Recommendations, TeamFavorites, VaultSearch, Profile
infra/
```

## Routes (Frontend)

- **/** — Recommendations (top by rating for user’s skill level)
- **/team-favorites** — Team favorites (5-star), own highlighted
- **/vault-search** — Full vault + filters
- **/profile** — User and team stats
