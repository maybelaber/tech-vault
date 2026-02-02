"""SkillLevels: full CRUD."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_reference_service
from app.models.core import User
from app.schemas.reference import SkillLevelRead, SkillLevelCreate, SkillLevelUpdate
from app.services import ReferenceService

router = APIRouter(prefix="/reference/skill-levels", tags=["skill-levels"])


@router.get("", response_model=list[SkillLevelRead])
async def list_skill_levels(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[SkillLevelRead]:
    return await svc.list_skill_levels()


@router.post("", response_model=SkillLevelRead, status_code=status.HTTP_201_CREATED)
async def create_skill_level(
    data: SkillLevelCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> SkillLevelRead:
    return await svc.create_skill_level(data)


@router.get("/{id}", response_model=SkillLevelRead)
async def get_skill_level(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> SkillLevelRead:
    s = await svc.get_skill_level(id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill level not found")
    return s


@router.put("/{id}", response_model=SkillLevelRead)
async def update_skill_level(
    id: UUID,
    data: SkillLevelUpdate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> SkillLevelRead:
    s = await svc.update_skill_level(id, data)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill level not found")
    return s


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill_level(
    id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> None:
    deleted = await svc.delete_skill_level(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill level not found")
