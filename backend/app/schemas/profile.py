"""Profile and stats schemas."""

from uuid import UUID

from pydantic import BaseModel


class TeamStats(BaseModel):
    team_id: UUID
    team_name: str
    uploaded_count: int
    ratings_count: int


class ProfileStats(BaseModel):
    user_id: UUID
    uploaded_count: int
    ratings_count: int
    team_stats: TeamStats | None = None


class MentorRead(BaseModel):
    """Mentor snippet for profile (My Mentors)."""

    id: UUID
    name: str
    role: str = "Mentor"
    username: str | None = None  # Telegram username for t.me link
