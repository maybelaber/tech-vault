"""Teams: full CRUD."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_reference_service
from app.models.core import User
from app.schemas.reference import TeamRead, TeamCreate, TeamUpdate
from app.services import ReferenceService

router = APIRouter(prefix="/reference/teams", tags=["teams"])


@router.get("", response_model=list[TeamRead])
async def list_teams(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[TeamRead]:
    return await svc.list_teams()


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    data: TeamCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TeamRead:
    return await svc.create_team(data)


@router.get("/{id}", response_model=TeamRead)
async def get_team(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TeamRead:
    t = await svc.get_team(id)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return t


@router.put("/{id}", response_model=TeamRead)
async def update_team(
    id: UUID,
    data: TeamUpdate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TeamRead:
    t = await svc.update_team(id, data)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return t


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> None:
    deleted = await svc.delete_team(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
