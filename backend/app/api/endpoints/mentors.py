"""Mentors: full CRUD."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_reference_service
from app.models.core import User
from app.schemas.reference import MentorRead, MentorCreate, MentorUpdate
from app.services import ReferenceService

router = APIRouter(prefix="/reference/mentors", tags=["mentors"])


@router.get("", response_model=list[MentorRead])
async def list_mentors(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[MentorRead]:
    return await svc.list_mentors()


@router.post("", response_model=MentorRead, status_code=status.HTTP_201_CREATED)
async def create_mentor(
    data: MentorCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> MentorRead:
    return await svc.create_mentor(data)


@router.get("/{id}", response_model=MentorRead)
async def get_mentor(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> MentorRead:
    m = await svc.get_mentor(id)
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")
    return m


@router.put("/{id}", response_model=MentorRead)
async def update_mentor(
    id: UUID,
    data: MentorUpdate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> MentorRead:
    m = await svc.update_mentor(id, data)
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")
    return m


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mentor(
    id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> None:
    deleted = await svc.delete_mentor(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")
