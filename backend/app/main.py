"""TechVault API — FastAPI app, CORS, health check."""

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api import health, auth, resources, ratings, recommendations, team_favorites, profile, favorites
from app.api.deps import get_current_user
from app.api.endpoints import auth as auth_endpoints, mentors, technologies, teams, skill_levels

import os
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # shutdown: close pool etc. if needed


app = FastAPI(
    title=settings.app_name,
    description="Corporate Knowledge Sharing Platform — Telegram Mini App",
    version="0.1.0",
    lifespan=lifespan,
)

origins_str = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173"]')

origins_raw = os.getenv("BACKEND_CORS_ORIGINS", "")
origins = [origin.strip() for origin in origins_raw.split(",") if origin]

if not origins:
    origins = ["http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public (no JWT required)
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(auth_endpoints.router, prefix="/api/auth")
app.include_router(technologies.router, prefix="/api")  # GET list/id public
app.include_router(mentors.router, prefix="/api")  # GET list/id public
app.include_router(teams.router, prefix="/api")  # GET list/id public
app.include_router(skill_levels.router, prefix="/api")  # GET list/id public

# Protected (JWT required); resources: create/update protected per-route
app.include_router(resources.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
app.include_router(
    ratings.router, prefix="/api", dependencies=[Depends(get_current_user)]
)
app.include_router(
    recommendations.router, prefix="/api", dependencies=[Depends(get_current_user)]
)
app.include_router(
    team_favorites.router, prefix="/api", dependencies=[Depends(get_current_user)]
)
app.include_router(
    profile.router, prefix="/api", dependencies=[Depends(get_current_user)]
)

# Serve static demo files from backend/static/demo at /demo (works locally and in Docker)
_base_dir = Path(__file__).resolve().parent.parent
_static_demo_dir = _base_dir / "static" / "demo"
_static_demo_dir.mkdir(parents=True, exist_ok=True)
app.mount("/demo", StaticFiles(directory=str(_static_demo_dir)), name="demo")


@app.get("/")
async def root() -> dict[str, str]:
    return {"app": "TechVault", "docs": "/docs"}
