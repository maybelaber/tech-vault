"""Favorite (like) repository: toggle and list for user_data.favorites."""

from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.core import Favorite, Resource

_RESOURCE_LOAD_OPTIONS = (
    joinedload(Resource.technology),
    joinedload(Resource.skill_level),
    joinedload(Resource.mentor),
)


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def has_favorite(self, user_id: UUID, resource_id: UUID) -> bool:
        result = await self._session.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.resource_id == resource_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_favorite_resource_ids(self, user_id: UUID) -> set[UUID]:
        result = await self._session.execute(
            select(Favorite.resource_id).where(Favorite.user_id == user_id)
        )
        return set(result.scalars().all())

    async def toggle_favorite(self, user_id: UUID, resource_id: UUID) -> bool:
        """If exists, delete; else create. Return new state (True = favorited)."""
        existing = await self._session.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.resource_id == resource_id,
            )
        )
        row = existing.scalar_one_or_none()
        if row:
            await self._session.delete(row)
            await self._session.flush()
            await self._session.commit()
            return False
        self._session.add(
            Favorite(user_id=user_id, resource_id=resource_id)
        )
        await self._session.flush()
        await self._session.commit()
        return True

    async def get_favorites(self, user_id: UUID) -> list[Resource]:
        q = (
            select(Resource)
            .join(Favorite, Favorite.resource_id == Resource.id)
            .where(Favorite.user_id == user_id)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .order_by(Favorite.created_at.desc())
        )
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())
