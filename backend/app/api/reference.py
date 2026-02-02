"""Reference data (read-only): technologies, mentors, teams, skill-levels."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_reference_service
from app.schemas.reference import (
    TechnologyRead,
    MentorRead,
    TeamRead,
    SkillLevelRead,
)
from app.services import ReferenceService

router = APIRouter(prefix="/reference", tags=["reference"])


@router.get("/technologies", response_model=list[TechnologyRead])
async def list_technologies(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[TechnologyRead]:
    return await svc.list_technologies()


@router.get("/technologies/{id}", response_model=TechnologyRead)
async def get_technology(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TechnologyRead:
    t = await svc.get_technology(id)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found")
    return t


@router.get("/mentors", response_model=list[MentorRead])
async def list_mentors(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[MentorRead]:
    return await svc.list_mentors()


@router.get("/mentors/{id}", response_model=MentorRead)
async def get_mentor(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> MentorRead:
    m = await svc.get_mentor(id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")
    return m


@router.get("/teams", response_model=list[TeamRead])
async def list_teams(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[TeamRead]:
    return await svc.list_teams()


@router.get("/teams/{id}", response_model=TeamRead)
async def get_team(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TeamRead:
    t = await svc.get_team(id)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return t


@router.get("/skill-levels", response_model=list[SkillLevelRead])
async def list_skill_levels(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[SkillLevelRead]:
    return await svc.list_skill_levels()


@router.get("/skill-levels/{id}", response_model=SkillLevelRead)
async def get_skill_level(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> SkillLevelRead:
    s = await svc.get_skill_level(id)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill level not found")
    return s
