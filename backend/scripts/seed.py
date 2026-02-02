#!/usr/bin/env python3
"""
Seed the database with demo data: 5 technologies, 3 skill levels, 2 mentors, 1 team,
1 demo user, and 10 resources. Run once for demo data.

Usage (from repo root):
  python backend/scripts/seed.py
Or from backend directory:
  cd backend && python scripts/seed.py
"""
import asyncio
import sys
from pathlib import Path

# Ensure backend is on path so "app" resolves
_backend = Path(__file__).resolve().parent.parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.core import Resource, ResourceType, User
from app.models.reference import Mentor, SkillLevel, Team, Technology


DEMO_TELEGRAM_ID = 999000111  # Demo user for seeding


async def has_seed_data(session: AsyncSession) -> bool:
    """Return True if reference data already exists (skip re-seeding)."""
    result = await session.execute(select(func.count()).select_from(Technology))
    return (result.scalar() or 0) > 0


async def seed(session: AsyncSession) -> None:
    if await has_seed_data(session):
        print("Seed data already present, skipping.")
        return
    # --- Reference: Technologies (5) ---
    techs_data = [
        ("Python", "Python programming language and ecosystem"),
        ("Kubernetes", "Container orchestration and cloud-native workloads"),
        ("React", "Frontend library for building user interfaces"),
        ("PostgreSQL", "Relational database management system"),
        ("Figma", "Design and prototyping tool"),
    ]
    technologies: list[Technology] = []
    for name, desc in techs_data:
        t = Technology(name=name, description=desc)
        session.add(t)
        technologies.append(t)
    await session.flush()

    # --- Reference: Skill levels (3) ---
    levels_data = [
        ("Junior", 1),
        ("Middle", 2),
        ("Senior", 3),
    ]
    skill_levels: list[SkillLevel] = []
    for name, order in levels_data:
        sl = SkillLevel(name=name, sort_order=order)
        session.add(sl)
        skill_levels.append(sl)
    await session.flush()

    # --- Reference: Mentors (2) ---
    mentors_data = [
        ("Alice Smith", "alice@example.com"),
        ("Bob Jones", "bob@example.com"),
    ]
    mentors: list[Mentor] = []
    for name, email in mentors_data:
        m = Mentor(name=name, email=email)
        session.add(m)
        mentors.append(m)
    await session.flush()

    # --- Reference: Team (1, optional for resources) ---
    team = Team(name="Platform Team", description="Backend and platform engineers")
    session.add(team)
    await session.flush()

    # --- User: demo uploader (1) ---
    result = await session.execute(select(User).where(User.telegram_id == DEMO_TELEGRAM_ID))
    demo_user = result.scalar_one_or_none()
    if demo_user is None:
        demo_user = User(
            telegram_id=DEMO_TELEGRAM_ID,
            username="demo_seed",
            first_name="Demo",
            last_name="User",
            team_id=team.id,
            skill_level_id=skill_levels[1].id,  # Middle
        )
        session.add(demo_user)
        await session.flush()

    # --- Resources (10), linked to techs, levels, mentors ---
    resources_data = [
        ("Python Style Guide", "PEP 8 and best practices for Python code.", ResourceType.DOC, 0, 0, 0),
        ("Kubernetes Quick Start", "Deploy your first pod and service.", ResourceType.DOC, 1, 0, 1),
        ("React Hooks Cheatsheet", "useState, useEffect, and custom hooks.", ResourceType.SNIPPET, 2, 0, 0),
        ("PostgreSQL Indexing", "When and how to add indexes.", ResourceType.BLUEPRINT, 3, 1, 2),
        ("Figma Components", "Reusable UI components in Figma.", ResourceType.DOC, 4, 1, 0),
        ("Python Async Patterns", "asyncio and async/await patterns.", ResourceType.SNIPPET, 0, 0, 2),
        ("K8s Helm Chart Template", "Template for a generic Helm chart.", ResourceType.BLUEPRINT, 1, 0, 1),
        ("React + TypeScript Setup", "Vite + React + TS project setup.", ResourceType.DOC, 2, 1, 1),
        ("PostgreSQL Migrations", "Alembic and migration workflow.", ResourceType.DOC, 3, 0, 0),
        ("Design Tokens in Figma", "Variables and design tokens.", ResourceType.DOC, 4, 1, 1),
    ]
    for title, desc, rtype, tech_idx, mentor_idx, level_idx in resources_data:
        r = Resource(
            uploader_id=demo_user.id,
            title=title,
            description=desc,
            file_path=f"/demo/{title.lower().replace(' ', '_')}.md",
            resource_type=rtype,
            technology_id=technologies[tech_idx].id,
            mentor_id=mentors[mentor_idx].id,
            team_id=team.id,
            skill_level_id=skill_levels[level_idx].id,
            average_rating=Decimal("4.20") if tech_idx % 2 == 0 else Decimal("3.80"),
            ratings_count=tech_idx + 1,
        )
        session.add(r)
    await session.flush()

    print("Seeded: 5 technologies, 3 skill levels, 2 mentors, 1 team, 1 user, 10 resources.")


async def main() -> None:
    async with AsyncSessionLocal() as session:
        try:
            await seed(session)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise SystemExit(f"Seed failed: {e}") from e


if __name__ == "__main__":
    asyncio.run(main())
