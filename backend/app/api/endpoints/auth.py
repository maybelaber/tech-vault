"""Telegram authentication: POST /api/auth/telegram."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, validate_telegram_hash
from app.repositories.user_repo import UserRepository
from app.schemas.telegram_auth import (
    TelegramLoginPayload,
    TelegramAuthResponse,
    UserResponse,
)

router = APIRouter(tags=["auth"])


@router.post("/telegram", response_model=TelegramAuthResponse)
async def auth_telegram(
    payload: TelegramLoginPayload,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> TelegramAuthResponse:
    """
    Validate Telegram Login Widget data and return JWT + user.
    If hash is invalid, returns 403.
    """
    if not settings.telegram_bot_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Telegram auth is not configured (missing TELEGRAM_BOT_TOKEN)",
        )
    payload_dict = payload.model_dump(exclude_none=True)
    if not validate_telegram_hash(payload_dict, settings.telegram_bot_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Telegram login hash",
        )
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(payload.id)
    if user is None:
        user = await user_repo.create(
            telegram_id=payload.id,
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
    else:
        await user_repo.update(
            user,
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
    access_token = create_access_token(str(user.id))
    return TelegramAuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )
