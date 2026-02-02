"""Rating repository. No deletion per TZ."""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.core import Rating, Resource
from decimal import Decimal


class RatingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_and_resource(
        self, user_id: UUID, resource_id: UUID
    ) -> Rating | None:
        result = await self._session.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.resource_id == resource_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, resource_id: UUID, score: int) -> Rating:
        rating = Rating(user_id=user_id, resource_id=resource_id, score=score)
        self._session.add(rating)
        await self._session.flush()
        await self._session.refresh(rating)
        return rating

    async def update_score(self, rating: Rating, score: int) -> Rating:
        rating.score = score
        await self._session.flush()
        await self._session.refresh(rating)
        return rating

    async def recalc_resource_rating(self, resource_id: UUID) -> None:
        """Recalculate average_rating and ratings_count for resource."""
        from sqlalchemy import update
        subq = (
            select(
                func.coalesce(func.avg(Rating.score), 0).label("avg"),
                func.count(Rating.id).label("cnt"),
            ).where(Rating.resource_id == resource_id)
        )
        result = await self._session.execute(subq)
        row = result.one()
        avg_val = float(row.avg) if row.avg is not None else 0.0
        cnt_val = row.cnt or 0
        await self._session.execute(
            update(Resource)
            .where(Resource.id == resource_id)
            .values(
                average_rating=Decimal(str(round(avg_val, 2))),
                ratings_count=cnt_val,
            )
        )
        await self._session.flush()

    async def count_by_user(self, user_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(Rating).where(Rating.user_id == user_id)
        )
        return result.scalar() or 0
