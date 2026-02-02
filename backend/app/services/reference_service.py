"""Reference data service: full CRUD for Technologies, Mentors, Teams, SkillLevels."""

from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.reference_repo import ReferenceRepository
from app.models.reference import Technology, Mentor, Team, SkillLevel
from app.schemas.reference import (
    TechnologyRead,
    TechnologyCreate,
    TechnologyUpdate,
    MentorRead,
    MentorCreate,
    MentorUpdate,
    TeamRead,
    TeamCreate,
    TeamUpdate,
    SkillLevelRead,
    SkillLevelCreate,
    SkillLevelUpdate,
)


class ReferenceService:
    def __init__(self, repo: ReferenceRepository) -> None:
        self._repo = repo

    # --- Technology ---
    async def list_technologies(self) -> list[TechnologyRead]:
        items = await self._repo.get_technologies()
        return [TechnologyRead.model_validate(t) for t in items]

    async def get_technology(self, id: UUID) -> TechnologyRead | None:
        t = await self._repo.get_technology(id)
        return TechnologyRead.model_validate(t) if t else None

    async def create_technology(self, data: TechnologyCreate) -> TechnologyRead:
        t = await self._repo.create_technology(
            name=data.name,
            description=data.description,
        )
        return TechnologyRead.model_validate(t)

    async def update_technology(self, id: UUID, data: TechnologyUpdate) -> TechnologyRead | None:
        t = await self._repo.get_technology(id)
        if not t:
            return None
        await self._repo.update_technology(
            t,
            name=data.name,
            description=data.description,
        )
        return TechnologyRead.model_validate(t)

    async def delete_technology(self, id: UUID) -> bool:
        return await self._repo.delete_technology(id)

    # --- Mentor ---
    async def list_mentors(self) -> list[MentorRead]:
        items = await self._repo.get_mentors()
        return [MentorRead.model_validate(m) for m in items]

    async def get_mentor(self, id: UUID) -> MentorRead | None:
        m = await self._repo.get_mentor(id)
        return MentorRead.model_validate(m) if m else None

    async def create_mentor(self, data: MentorCreate) -> MentorRead:
        m = await self._repo.create_mentor(
            name=data.name,
            email=data.email,
        )
        return MentorRead.model_validate(m)

    async def update_mentor(self, id: UUID, data: MentorUpdate) -> MentorRead | None:
        m = await self._repo.get_mentor(id)
        if not m:
            return None
        await self._repo.update_mentor(m, name=data.name, email=data.email)
        return MentorRead.model_validate(m)

    async def delete_mentor(self, id: UUID) -> bool:
        return await self._repo.delete_mentor(id)

    # --- Team ---
    async def list_teams(self) -> list[TeamRead]:
        items = await self._repo.get_teams()
        return [TeamRead.model_validate(t) for t in items]

    async def get_team(self, id: UUID) -> TeamRead | None:
        t = await self._repo.get_team(id)
        return TeamRead.model_validate(t) if t else None

    async def create_team(self, data: TeamCreate) -> TeamRead:
        t = await self._repo.create_team(
            name=data.name,
            description=data.description,
        )
        return TeamRead.model_validate(t)

    async def update_team(self, id: UUID, data: TeamUpdate) -> TeamRead | None:
        t = await self._repo.get_team(id)
        if not t:
            return None
        await self._repo.update_team(t, name=data.name, description=data.description)
        return TeamRead.model_validate(t)

    async def delete_team(self, id: UUID) -> bool:
        return await self._repo.delete_team(id)

    # --- SkillLevel ---
    async def list_skill_levels(self) -> list[SkillLevelRead]:
        items = await self._repo.get_skill_levels()
        return [SkillLevelRead.model_validate(s) for s in items]

    async def get_skill_level(self, id: UUID) -> SkillLevelRead | None:
        s = await self._repo.get_skill_level(id)
        return SkillLevelRead.model_validate(s) if s else None

    async def create_skill_level(self, data: SkillLevelCreate) -> SkillLevelRead:
        s = await self._repo.create_skill_level(
            name=data.name,
            sort_order=data.sort_order,
        )
        return SkillLevelRead.model_validate(s)

    async def update_skill_level(self, id: UUID, data: SkillLevelUpdate) -> SkillLevelRead | None:
        s = await self._repo.get_skill_level(id)
        if not s:
            return None
        await self._repo.update_skill_level(
            s,
            name=data.name,
            sort_order=data.sort_order,
        )
        return SkillLevelRead.model_validate(s)

    async def delete_skill_level(self, id: UUID) -> bool:
        return await self._repo.delete_skill_level(id)
