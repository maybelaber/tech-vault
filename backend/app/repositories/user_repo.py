"""User repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.core import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> User | None:
        result = await self._session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int, username: str | None = None,
                     first_name: str | None = None, last_name: str | None = None,
                     team_id: UUID | None = None, skill_level_id: UUID | None = None) -> User:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            team_id=team_id,
            skill_level_id=skill_level_id,
        )
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update(self, user: User, *, username: str | None = None,
                     first_name: str | None = None, last_name: str | None = None,
                     team_id: UUID | None = None, skill_level_id: UUID | None = None) -> User:
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if team_id is not None:
            user.team_id = team_id
        if skill_level_id is not None:
            user.skill_level_id = skill_level_id
        await self._session.flush()
        await self._session.refresh(user)
        return user
