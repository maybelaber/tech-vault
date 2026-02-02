"""Resource (doc/blueprint/snippet) service."""

from uuid import UUID

from app.repositories.resource_repo import ResourceRepository
from app.models.core import Resource, ResourceType
from app.schemas.resource import (
    ResourceRead,
    ResourceCreate,
    ResourceUpdate,
    ResourceFilters,
    ResourceTypeEnum,
)


def _resource_type_enum_to_model(e: ResourceTypeEnum) -> ResourceType:
    return ResourceType(e.value)


class ResourceService:
    def __init__(self, repo: ResourceRepository) -> None:
        self._repo = repo

    async def get_by_id(self, id: UUID) -> ResourceRead | None:
        r = await self._repo.get_by_id(id)
        return ResourceRead.model_validate(r) if r else None

    async def list_filtered(self, filters: ResourceFilters) -> list[ResourceRead]:
        items = await self._repo.list_filtered(filters)
        return [ResourceRead.model_validate(r) for r in items]

    async def create(self, uploader_id: UUID, data: ResourceCreate) -> ResourceRead:
        r = await self._repo.create(
            uploader_id=uploader_id,
            title=data.title,
            description=data.description,
            file_path=data.file_path,
            resource_type=_resource_type_enum_to_model(data.resource_type),
            technology_id=data.technology_id,
            mentor_id=data.mentor_id,
            team_id=data.team_id,
            skill_level_id=data.skill_level_id,
        )
        return ResourceRead.model_validate(r)

    async def update(self, id: UUID, data: ResourceUpdate) -> ResourceRead | None:
        r = await self._repo.get_by_id(id)
        if not r:
            return None
        return ResourceRead.model_validate(
            await self._repo.update(r, data)
        )

    async def list_top_for_skill_level(
        self, skill_level_id: UUID, limit: int = 50
    ) -> list[ResourceRead]:
        items = await self._repo.list_top_by_rating_for_skill_level(
            skill_level_id, limit=limit
        )
        return [ResourceRead.model_validate(r) for r in items]

    async def list_team_favorites(self, team_id: UUID, limit: int = 100) -> list[ResourceRead]:
        items = await self._repo.list_team_favorites(team_id, limit=limit)
        return [ResourceRead.model_validate(r) for r in items]
