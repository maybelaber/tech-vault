"""User (employee) service."""

from uuid import UUID

from app.repositories.user_repo import UserRepository
from app.models.core import User
from app.schemas.user import UserRead, UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def get_by_id(self, id: UUID) -> UserRead | None:
        user = await self._repo.get_by_id(id)
        return UserRead.model_validate(user) if user else None

    async def get_by_telegram_id(self, telegram_id: int) -> UserRead | None:
        user = await self._repo.get_by_telegram_id(telegram_id)
        return UserRead.model_validate(user) if user else None

    async def get_or_create(self, data: UserCreate) -> User:
        user = await self._repo.get_by_telegram_id(data.telegram_id)
        if user:
            return user
        return await self._repo.create(
            telegram_id=data.telegram_id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            team_id=data.team_id,
            skill_level_id=data.skill_level_id,
        )

    async def update(self, user: User, data: UserUpdate) -> User:
        return await self._repo.update(
            user,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            team_id=data.team_id,
            skill_level_id=data.skill_level_id,
        )
