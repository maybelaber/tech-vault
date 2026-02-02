"""Rating service. No deletion per TZ — create or update only."""

from uuid import UUID

from app.repositories.rating_repo import RatingRepository
from app.models.core import User, Resource
from app.schemas.rating import RatingRead, RateResponse
from decimal import Decimal


class RatingService:
    def __init__(self, repo: RatingRepository) -> None:
        self._repo = repo

    async def get_for_user_and_resource(
        self, user_id: UUID, resource_id: UUID
    ) -> RatingRead | None:
        r = await self._repo.get_by_user_and_resource(user_id, resource_id)
        return RatingRead.model_validate(r) if r else None

    async def set_rating(self, user: User, resource_id: UUID, score: int) -> RateResponse:
        """Create or update rating (1–5). Recalculates resource average. Returns new stats."""
        resource = await self._repo._session.get(Resource, resource_id)
        if not resource:
            raise ValueError("Resource not found")
        existing = await self._repo.get_by_user_and_resource(user.id, resource_id)
        if existing:
            await self._repo.update_score(existing, score)
        else:
            await self._repo.create(user.id, resource_id, score)
        await self._repo.recalc_resource_rating(resource_id)
        await self._repo._session.refresh(resource)
        return RateResponse(
            average_rating=resource.average_rating,
            ratings_count=resource.ratings_count,
            user_rating=score,
        )
