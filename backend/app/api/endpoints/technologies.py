"""Technologies: full CRUD."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_reference_service
from app.models.core import User
from app.schemas.reference import TechnologyRead, TechnologyCreate, TechnologyUpdate
from app.services import ReferenceService

router = APIRouter(prefix="/reference/technologies", tags=["technologies"])


@router.get("", response_model=list[TechnologyRead])
async def list_technologies(
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> list[TechnologyRead]:
    return await svc.list_technologies()


@router.post("", response_model=TechnologyRead, status_code=status.HTTP_201_CREATED)
async def create_technology(
    data: TechnologyCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TechnologyRead:
    return await svc.create_technology(data)


@router.get("/{id}", response_model=TechnologyRead)
async def get_technology(
    id: UUID,
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TechnologyRead:
    t = await svc.get_technology(id)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found")
    return t


@router.put("/{id}", response_model=TechnologyRead)
async def update_technology(
    id: UUID,
    data: TechnologyUpdate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> TechnologyRead:
    t = await svc.update_technology(id, data)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found")
    return t


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technology(
    id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ReferenceService, Depends(get_reference_service)],
) -> None:
    deleted = await svc.delete_technology(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found")
