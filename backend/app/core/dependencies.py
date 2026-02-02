"""FastAPI dependencies: DB session, repos, services, auth."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import (
    ReferenceRepository,
    UserRepository,
    ResourceRepository,
    RatingRepository,
    FavoriteRepository,
)
from app.services import (
    ReferenceService,
    UserService,
    ResourceService,
    RatingService,
    RecommendationService,
    ProfileService,
)
from app.models.core import User


async def get_reference_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ReferenceRepository:
    return ReferenceRepository(session)


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(session)


async def get_resource_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ResourceRepository:
    return ResourceRepository(session)


async def get_rating_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> RatingRepository:
    return RatingRepository(session)


async def get_favorite_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> FavoriteRepository:
    return FavoriteRepository(session)


# Services (inject repos)
async def get_reference_service(
    repo: Annotated[ReferenceRepository, Depends(get_reference_repo)],
) -> ReferenceService:
    return ReferenceService(repo)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


async def get_resource_service(
    repo: Annotated[ResourceRepository, Depends(get_resource_repo)],
) -> ResourceService:
    return ResourceService(repo)


async def get_rating_service(
    repo: Annotated[RatingRepository, Depends(get_rating_repo)],
) -> RatingService:
    return RatingService(repo)


async def get_recommendation_service(
    resource_repo: Annotated[ResourceRepository, Depends(get_resource_repo)],
) -> RecommendationService:
    return RecommendationService(resource_repo)


async def get_profile_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    resource_repo: Annotated[ResourceRepository, Depends(get_resource_repo)],
    rating_repo: Annotated[RatingRepository, Depends(get_rating_repo)],
    reference_repo: Annotated[ReferenceRepository, Depends(get_reference_repo)],
    favorite_repo: Annotated[FavoriteRepository, Depends(get_favorite_repo)],
) -> ProfileService:
    return ProfileService(
        user_repo, resource_repo, rating_repo, reference_repo, favorite_repo
    )


# Auth: validate Telegram initData (stub — returns user by X-Telegram-User-Id for dev)
TELEGRAM_INIT_DATA_HEADER = "X-Telegram-Init-Data"
TELEGRAM_USER_ID_HEADER = "X-Telegram-User-Id"


async def get_current_user_optional(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    x_telegram_user_id: str | None = Header(None, alias=TELEGRAM_USER_ID_HEADER),
) -> User | None:
    """Optional auth: if X-Telegram-User-Id present, return user (for dev). Real auth validates initData."""
    if x_telegram_user_id is None:
        return None
    try:
        tid = int(x_telegram_user_id)
    except ValueError:
        return None
    return await user_repo.get_by_telegram_id(tid)


async def get_current_user(
    user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User:
    """Required auth: 401 if not authenticated."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide valid Telegram initData or X-Telegram-User-Id.",
        )
    return user


# Type aliases for route injection
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
