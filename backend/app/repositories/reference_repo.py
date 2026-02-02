"""Reference data repository: CRUD for Technologies, Mentors, Teams, SkillLevels."""

from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reference import Technology, Mentor, Team, SkillLevel


class ReferenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # --- Technology ---
    async def get_technologies(self) -> list[Technology]:
        result = await self._session.execute(select(Technology).order_by(Technology.name))
        return list(result.scalars().all())

    async def get_technology(self, id: UUID) -> Technology | None:
        result = await self._session.execute(select(Technology).where(Technology.id == id))
        return result.scalar_one_or_none()

    async def create_technology(self, *, name: str, description: str | None = None) -> Technology:
        obj = Technology(name=name, description=description)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update_technology(
        self, obj: Technology, *, name: str | None = None, description: str | None = None
    ) -> Technology:
        if name is not None:
            obj.name = name
        if description is not None:
            obj.description = description
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete_technology(self, id: UUID) -> bool:
        result = await self._session.execute(delete(Technology).where(Technology.id == id))
        await self._session.flush()
        return result.rowcount > 0

    # --- Mentor ---
    async def get_mentors(self) -> list[Mentor]:
        result = await self._session.execute(select(Mentor).order_by(Mentor.name))
        return list(result.scalars().all())

    async def get_mentor(self, id: UUID) -> Mentor | None:
        result = await self._session.execute(select(Mentor).where(Mentor.id == id))
        return result.scalar_one_or_none()

    async def create_mentor(self, *, name: str, email: str | None = None) -> Mentor:
        obj = Mentor(name=name, email=email)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update_mentor(
        self, obj: Mentor, *, name: str | None = None, email: str | None = None
    ) -> Mentor:
        if name is not None:
            obj.name = name
        if email is not None:
            obj.email = email
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete_mentor(self, id: UUID) -> bool:
        result = await self._session.execute(delete(Mentor).where(Mentor.id == id))
        await self._session.flush()
        return result.rowcount > 0

    # --- Team ---
    async def get_teams(self) -> list[Team]:
        result = await self._session.execute(select(Team).order_by(Team.name))
        return list(result.scalars().all())

    async def get_team(self, id: UUID) -> Team | None:
        result = await self._session.execute(select(Team).where(Team.id == id))
        return result.scalar_one_or_none()

    async def create_team(self, *, name: str, description: str | None = None) -> Team:
        obj = Team(name=name, description=description)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update_team(
        self, obj: Team, *, name: str | None = None, description: str | None = None
    ) -> Team:
        if name is not None:
            obj.name = name
        if description is not None:
            obj.description = description
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete_team(self, id: UUID) -> bool:
        result = await self._session.execute(delete(Team).where(Team.id == id))
        await self._session.flush()
        return result.rowcount > 0

    # --- SkillLevel ---
    async def get_skill_levels(self) -> list[SkillLevel]:
        result = await self._session.execute(
            select(SkillLevel).order_by(SkillLevel.sort_order, SkillLevel.name)
        )
        return list(result.scalars().all())

    async def get_skill_level(self, id: UUID) -> SkillLevel | None:
        result = await self._session.execute(
            select(SkillLevel).where(SkillLevel.id == id)
        )
        return result.scalar_one_or_none()

    async def create_skill_level(self, *, name: str, sort_order: int = 0) -> SkillLevel:
        obj = SkillLevel(name=name, sort_order=sort_order)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update_skill_level(
        self, obj: SkillLevel, *, name: str | None = None, sort_order: int | None = None
    ) -> SkillLevel:
        if name is not None:
            obj.name = name
        if sort_order is not None:
            obj.sort_order = sort_order
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete_skill_level(self, id: UUID) -> bool:
        result = await self._session.execute(delete(SkillLevel).where(SkillLevel.id == id))
        await self._session.flush()
        return result.rowcount > 0
