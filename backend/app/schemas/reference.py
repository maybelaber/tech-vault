"""Reference data schemas: Response (Read), Create, Update."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# --- Technology ---
class TechnologyRead(BaseModel):
    """Response schema for Technology."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    created_at: datetime


class TechnologyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TechnologyUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


# --- Mentor ---
class MentorRead(BaseModel):
    """Response schema for Mentor."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str | None = None
    created_at: datetime


class MentorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str | None = Field(None, max_length=255)


class MentorUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    email: str | None = Field(None, max_length=255)


# --- Team ---
class TeamRead(BaseModel):
    """Response schema for Team."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    created_at: datetime


class TeamCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


# --- SkillLevel ---
class SkillLevelRead(BaseModel):
    """Response schema for SkillLevel."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    sort_order: int = 0
    created_at: datetime


class SkillLevelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    sort_order: int = 0


class SkillLevelUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=64)
    sort_order: int | None = None
