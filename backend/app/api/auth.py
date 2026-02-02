"""Auth: Telegram initData (stub), get/create user."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service, get_current_user_optional
from app.schemas.user import UserRead, UserCreate
from app.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserRead | None)
async def get_me(
    user: Annotated[None, Depends(get_current_user_optional)],
) -> UserRead | None:
    """Current user from X-Telegram-User-Id (dev). None if not authenticated."""
    if user is None:
        return None
    return UserRead.model_validate(user)


@router.post("/login", response_model=UserRead)
async def login(
    data: UserCreate,
    user_svc: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Register or get user by telegram_id. Production: validate initData and extract user."""
    user = await user_svc.get_or_create(data)
    return UserRead.model_validate(user)
