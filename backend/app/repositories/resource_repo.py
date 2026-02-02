"""Resource repository: CRUD and list for user_data.resources."""

from uuid import UUID

from sqlalchemy import or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.core import Resource, ResourceType, Rating
from app.schemas.resource import ResourceFilters, ResourceTypeEnum, ResourceUpdate


def _resource_type_from_enum(e: ResourceTypeEnum) -> ResourceType:
    return ResourceType(e.value)


# Eager-load relationships so ResourceRead (technology, skill_level, mentor) serializes without lazy load
_RESOURCE_LOAD_OPTIONS = (
    joinedload(Resource.technology),
    joinedload(Resource.skill_level),
    joinedload(Resource.mentor),
)


class ResourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> Resource | None:
        result = await self._session.execute(
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .where(Resource.id == id)
        )
        return result.unique().scalar_one_or_none()

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Resource]:
        result = await self._session.execute(
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .order_by(Resource.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.unique().scalars().all())

    async def list_filtered(self, filters: ResourceFilters) -> list[Resource]:
        q = (
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .order_by(Resource.created_at.desc())
        )
        if filters.search:
            pattern = f"%{filters.search}%"
            q = q.where(
                or_(
                    Resource.title.ilike(pattern),
                    Resource.description.ilike(pattern),
                )
            )
        if filters.team_id is not None:
            q = q.where(Resource.team_id == filters.team_id)
        if filters.skill_level_id is not None:
            q = q.where(Resource.skill_level_id == filters.skill_level_id)
        if filters.mentor_id is not None:
            q = q.where(Resource.mentor_id == filters.mentor_id)
        if filters.technology_id is not None:
            q = q.where(Resource.technology_id == filters.technology_id)
        if filters.resource_type is not None:
            q = q.where(Resource.resource_type == _resource_type_from_enum(filters.resource_type))
        q = q.offset(filters.offset).limit(filters.limit)
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())

    async def list_top_by_rating_for_skill_level(
        self, skill_level_id: UUID, limit: int = 50
    ) -> list[Resource]:
        q = (
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .where(Resource.skill_level_id == skill_level_id)
            .where(Resource.ratings_count > 0)
            .order_by(Resource.average_rating.desc(), Resource.ratings_count.desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())

    async def list_newest(self, limit: int = 3) -> list[Resource]:
        q = (
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .order_by(Resource.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())

    async def list_most_popular(self, limit: int = 3) -> list[Resource]:
        q = (
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .where(Resource.ratings_count > 0)
            .order_by(Resource.average_rating.desc(), Resource.ratings_count.desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())

    async def list_team_favorites(self, team_id: UUID, limit: int = 100) -> list[Resource]:
        subq = select(Rating.resource_id).where(Rating.score == 5).distinct()
        q = (
            select(Resource)
            .options(*_RESOURCE_LOAD_OPTIONS)
            .where(Resource.team_id == team_id)
            .where(Resource.id.in_(subq))
            .order_by(Resource.updated_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(q)
        return list(result.unique().scalars().all())

    async def create(
        self,
        uploader_id: UUID,
        *,
        title: str,
        description: str | None = None,
        file_path: str = "",
        resource_type: ResourceType = ResourceType.DOC,
        technology_id: UUID | None = None,
        mentor_id: UUID | None = None,
        team_id: UUID | None = None,
        skill_level_id: UUID | None = None,
    ) -> Resource:
        r = Resource(
            uploader_id=uploader_id,
            title=title,
            description=description,
            file_path=file_path,
            resource_type=resource_type,
            technology_id=technology_id,
            mentor_id=mentor_id,
            team_id=team_id,
            skill_level_id=skill_level_id,
        )
        self._session.add(r)
        await self._session.flush()
        await self._session.refresh(r)
        return r

    async def count_by_uploader(self, uploader_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(Resource).where(Resource.uploader_id == uploader_id)
        )
        return result.scalar() or 0

    async def update(self, resource: Resource, data: ResourceUpdate) -> Resource:
        if data.title is not None:
            resource.title = data.title
        if data.description is not None:
            resource.description = data.description
        if data.file_path is not None:
            resource.file_path = data.file_path
        if data.resource_type is not None:
            resource.resource_type = _resource_type_from_enum(data.resource_type)
        if data.technology_id is not None:
            resource.technology_id = data.technology_id
        if data.mentor_id is not None:
            resource.mentor_id = data.mentor_id
        if data.team_id is not None:
            resource.team_id = data.team_id
        if data.skill_level_id is not None:
            resource.skill_level_id = data.skill_level_id
        await self._session.flush()
        await self._session.refresh(resource)
        return resource
