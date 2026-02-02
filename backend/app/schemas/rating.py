"""Rating (5-star) schemas. No deletion per TZ."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RatingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    resource_id: UUID
    score: int
    rating_date: datetime


class RatingCreate(BaseModel):
    resource_id: UUID
    score: int = Field(..., ge=1, le=5)


class RatingUpdate(BaseModel):
    score: int = Field(..., ge=1, le=5)


class RateBody(BaseModel):
    """POST /resources/{id}/rate body. Use 'value' for API consistency."""

    value: int = Field(..., ge=1, le=5, description="Star rating 1-5")


class RateResponse(BaseModel):
    """Response after setting rating: new resource stats."""

    average_rating: Decimal
    ratings_count: int
    user_rating: int  # the score just set
