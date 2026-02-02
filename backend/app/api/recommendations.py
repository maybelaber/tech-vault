"""Recommendations: top resources by rating for user's skill level."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.core.dependencies import get_recommendation_service
from app.models.core import User
from app.schemas.resource import ResourceRead
from app.services import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[ResourceRead])
async def get_recommendations(
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[RecommendationService, Depends(get_recommendation_service)],
    limit: int = Query(50, ge=1, le=100),
) -> list[ResourceRead]:
    """Top resources by average_rating for user's skill_level."""
    return await svc.get_recommendations(user, limit=limit)
