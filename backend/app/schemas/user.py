"""User (employee) schemas."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.profile import MentorRead


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class UserProfile(UserRead):
    """Profile with stats, skills (from favorites), and mentors."""

    stats: dict
    skills: List[str] = []  # Unique technology names from user's favorites
    mentors: List[MentorRead]
    mentors_personalized: bool = False  # True = from favorites ("Your Mentors"), False = fallback ("Recommended Mentors")


class UserCreate(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None
