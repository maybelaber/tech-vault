"""Telegram Login Widget payload and auth response."""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TelegramLoginPayload(BaseModel):
    """Data object returned by the Telegram Login Widget."""

    id: int = Field(..., description="Telegram user id")
    first_name: str = Field(..., max_length=255)
    last_name: str | None = Field(None, max_length=255)
    username: str | None = Field(None, max_length=255)
    photo_url: str | None = Field(None, max_length=512)
    auth_date: int = Field(..., description="Unix timestamp")
    hash: str = Field(..., description="HMAC-SHA256 hash to verify")


class UserResponse(BaseModel):
    """User object in auth response."""

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


class TelegramAuthResponse(BaseModel):
    """Response of POST /api/auth/telegram."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
