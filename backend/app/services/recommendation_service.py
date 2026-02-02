"""Recommendations: hybrid of newest + most popular resources."""

from app.repositories.resource_repo import ResourceRepository
from app.models.core import User, Resource
from app.schemas.resource import ResourceRead


class RecommendationService:
    def __init__(self, resource_repo: ResourceRepository) -> None:
        self._repo = resource_repo

    async def get_recommendations(
        self, user: User | None, limit: int = 50
    ) -> list[ResourceRead]:
        """
        Hybrid: 3 newest + 3 most popular, deduplicated.
        Safe when DB is empty (returns []).
        """
        newest = await self._repo.list_newest(limit=3)
        popular = await self._repo.list_most_popular(limit=3)

        seen_ids = set()
        combined: list[Resource] = []
        for r in newest:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                combined.append(r)
        for r in popular:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                combined.append(r)

        return [ResourceRead.model_validate(r) for r in combined[:limit]]
