"""Resource (doc/blueprint/snippet) schemas."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ResourceTypeEnum(str, Enum):
    doc = "doc"
    blueprint = "blueprint"
    snippet = "snippet"


class TechnologyNested(BaseModel):
    """Technology snippet for list/detail: id, name."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class SkillLevelNested(BaseModel):
    """Skill level snippet for list/detail: id, name."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class MentorNested(BaseModel):
    """Mentor snippet for resource detail: id, name split into first/last, role, avatar."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    role: str = "Mentor"
    avatar_url: Optional[str] = None

    @model_validator(mode="wrap")
    @classmethod
    def from_mentor_orm(cls, v, handler):
        if v is None:
            return None
        if hasattr(v, "name") and hasattr(v, "id"):
            name = (getattr(v, "name") or "").strip()
            parts = name.split(maxsplit=1)
            first = parts[0] if parts else ""
            last = parts[1] if len(parts) > 1 else ""
            return cls(
                id=getattr(v, "id"),
                first_name=first,
                last_name=last,
                role=getattr(v, "role", None) or "Mentor",
                avatar_url=getattr(v, "avatar_url", None),
            )
        return handler(v)


class ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    uploader_id: UUID
    title: str
    description: str | None = None
    file_path: str
    resource_type: ResourceTypeEnum
    technology_id: UUID | None = None
    mentor_id: UUID | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None
    average_rating: Decimal
    ratings_count: int
    created_at: datetime
    updated_at: datetime
    meta: dict | None = None
    technology: Optional[TechnologyNested] = None
    skill_level: Optional[SkillLevelNested] = None
    mentor: Optional[MentorNested] = None
    is_favorite: bool = False
    user_rating: int | None = None  # current user's rating 1-5, if any


class ResourceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=512)
    description: str | None = None
    file_path: str = Field(..., min_length=1, max_length=1024)
    resource_type: ResourceTypeEnum = ResourceTypeEnum.doc
    technology_id: UUID | None = None
    mentor_id: UUID | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None


class ResourceUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=512)
    description: str | None = None
    file_path: str | None = Field(None, min_length=1, max_length=1024)
    resource_type: ResourceTypeEnum | None = None
    technology_id: UUID | None = None
    mentor_id: UUID | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None


class ResourceFilters(BaseModel):
    search: str | None = None
    team_id: UUID | None = None
    skill_level_id: UUID | None = None
    mentor_id: UUID | None = None
    technology_id: UUID | None = None
    resource_type: ResourceTypeEnum | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
