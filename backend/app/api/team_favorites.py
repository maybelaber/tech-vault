"""Team favorites: resources with at least one 5-star from same team."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user
from app.core.dependencies import get_resource_service
from app.models.core import User
from app.schemas.resource import ResourceRead
from app.services import ResourceService

router = APIRouter(prefix="/team-favorites", tags=["team-favorites"])


@router.get("", response_model=list[ResourceRead])
async def get_team_favorites(
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ResourceService, Depends(get_resource_service)],
    limit: int = Query(100, ge=1, le=200),
) -> list[ResourceRead]:
    """Resources in user's team that have at least one 5-star. Requires user.team_id."""
    if user.team_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Set team to see team favorites",
        )
    return await svc.list_team_favorites(user.team_id, limit=limit)
