"""Ratings: set 1–5 (create or update). No deletion per TZ."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_rating_service
from app.models.core import User
from app.schemas.rating import RateBody, RateResponse
from app.services import RatingService

router = APIRouter(prefix="/resources", tags=["ratings"])


@router.post("/{resource_id}/rate", response_model=RateResponse)
async def post_rate(
    resource_id: UUID,
    body: RateBody,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[RatingService, Depends(get_rating_service)],
) -> RateResponse:
    """Set rating 1–5 for resource. Creates or updates; returns new average stats."""
    try:
        return await svc.set_rating(user, resource_id, body.value)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
