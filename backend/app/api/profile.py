"""Profile: user, stats, and mentors."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.dependencies import get_profile_service
from app.models.core import User
from app.schemas.user import UserProfile
from app.services import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserProfile)
async def get_profile(
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ProfileService, Depends(get_profile_service)],
) -> UserProfile:
    """User profile with stats and mentors."""
    return await svc.get_profile(user)
