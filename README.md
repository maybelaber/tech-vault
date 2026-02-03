# 🚀 TechVault — Enterprise Knowledge Management Ecosystem

**TechVault** is a scalable, corporate-grade platform designed to streamline knowledge sharing, technical onboarding, and mentorship coordination within engineering teams.

Unlike standard wiki systems, TechVault bridges the gap between **static documentation** and **interactive mentorship**, creating a unified ecosystem where developers can grow from "Junior" to "Senior" through structured learning paths and automated mentor matching.

![Dashboard Preview](./assets/dashboard.png)

---

## 🌐 Live Deployment (Demo)

The project is deployed in a production-like environment to demonstrate stability, performance, and CI/CD capabilities.

- **Live App (Frontend):** [https://tech-vault-six.vercel.app](https://tech-vault-six.vercel.app)
- **API Documentation (Swagger UI):** [https://tech-vault.onrender.com/docs](https://tech-vault.onrender.com/docs)

---

## 🏗 Architecture & System Design

The platform is built on a **Microservice-ready architecture**, utilizing modern asynchronous Python standards, strict type safety, and containerized deployment. It solves the "Documentation vs. Application" problem by serving both dynamic API data and static resources through a unified gateway.

### 🛠 Tech Stack

**Backend Core**

- **Framework:** FastAPI (Python 3.11+) — High-performance Async I/O.
- **Database:** PostgreSQL 16 (via Neon/Docker) — Managed with **SQLAlchemy 2.0 (Async)**.
- **Migrations:** Alembic — Version control for database schema.
- **Validation:** Pydantic V2 — Strict data parsing & serialization.
- **Auth:** JWT (Access/Refresh strategy) + **Telegram OAuth Widget**.

**Frontend Client**

- **Framework:** React 18 + Vite.
- **Language:** TypeScript (Strict Mode).
- **State:** React Hooks / Context API.
- **UI/UX:** TailwindCSS + Framer Motion.

**DevOps & Infrastructure**

- **Containerization:** Docker & Docker Compose (Multi-stage builds).
- **Networking:** Nginx / Vite Proxy (handling `/api` and static `/demo` routing).
- **Deployment:** Render (Backend) + Vercel (Frontend).

---

## ✨ Key Features

### 🔐 Hybrid Authentication System

Secure, passwordless login via **Telegram Widget integration**. The system validates hashes on the backend to prevent spoofing, issuing JWT tokens for session management.

### 👥 Intelligent Mentorship Matching

Automated logic links Mentees with Mentors based on:

- **Tech Stack Overlap** (e.g., Python, React).
- **Skill Gap Analysis** (Junior matches with Senior/Lead).
- **Availability Status**.

### 📂 Hybrid Content Delivery

TechVault implements a specialized file serving strategy:

- **Dynamic Data:** User profiles, mentorship requests (via REST API).
- **Static Resources:** Markdown guides and documentation served directly from the backend's file system, optimized for caching.

---

## 🚀 Getting Started (Local Development)

Follow these steps to deploy the full environment locally using Docker.

### 1. Prerequisites

- Docker Desktop & Docker Compose (v2.0+)
- Git

### 2. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/techvault.git
cd techvault
```

### 3. Environment Configuration

Create a `.env` file in the root directory.

```ini
# --- Database (Docker Internal Network) ---
# We use 'postgres' as the hostname because containers talk via Docker DNS
DATABASE_URL=postgresql+asyncpg://techvault:secret@postgres:5432/techvault

# --- Security ---
SECRET_KEY=change_this_to_a_strong_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# --- Integration ---
# Telegram Bot Token (Get from @BotFather)
BOT_TOKEN=your_telegram_bot_token

# --- Frontend Configuration ---
# Local Docker proxy setup
VITE_API_URL=/api
```

### 4. Launch Application

Start the entire stack (Database + Backend + Frontend). The build flag ensures dependencies are fresh.

```bash
docker-compose up --build
```

### 5. Access Points

- **Frontend App:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger Documentation:** http://localhost:8000/docs

---

## 🧪 Seeding Demo Data

To populate the database with realistic test data (Technologies, Skill Levels, Dummy Mentors), run the included seeder script inside the container:

**Windows (PowerShell):**

```powershell
docker-compose exec backend python scripts/seed.py
```

**Linux / macOS:**

```bash
docker-compose exec backend python3 scripts/seed.py
```

---

## 👤 Author

**Andrew**

- **Role:** Lead Backend Engineer / Architect
- **Focus:** Python, FastAPI, Cloud Architecture
- [GitHub Profile](https://github.com/maybelaber)
- [LinkedIn](https://linkedin.com/in/andrii-borysov-9945bb3aa/)
