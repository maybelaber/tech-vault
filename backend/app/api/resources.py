"""Resources (docs/blueprints/snippets): CRUD, list with filters (vault search)."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user, get_current_user_optional
from app.core.dependencies import get_resource_service, get_favorite_repo, get_rating_repo
from app.models.core import User
from app.repositories.favorite_repo import FavoriteRepository
from app.repositories.rating_repo import RatingRepository
from app.schemas.resource import ResourceRead, ResourceCreate, ResourceUpdate, ResourceFilters, ResourceTypeEnum
from app.services import ResourceService

router = APIRouter(prefix="/resources", tags=["resources"])


def _with_is_favorite(
    read: ResourceRead,
    resource_id: UUID,
    favorite_ids: set[UUID],
) -> ResourceRead:
    return read.model_copy(update={"is_favorite": resource_id in favorite_ids})


@router.get("", response_model=list[ResourceRead])
async def list_resources(
    search: str | None = Query(None, description="Filter by title or description (case-insensitive)"),
    team_id: UUID | None = None,
    skill_level_id: UUID | None = None,
    mentor_id: UUID | None = None,
    technology_id: UUID | None = None,
    resource_type: ResourceTypeEnum | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: Annotated[ResourceService, Depends(get_resource_service)] = ...,
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
    fav_repo: Annotated[FavoriteRepository, Depends(get_favorite_repo)] = ...,
) -> list[ResourceRead]:
    """Vault search: list resources with optional filters."""
    filters = ResourceFilters(
        search=search.strip() if search and search.strip() else None,
        team_id=team_id,
        skill_level_id=skill_level_id,
        mentor_id=mentor_id,
        technology_id=technology_id,
        resource_type=resource_type,
        limit=limit,
        offset=offset,
    )
    items = await svc.list_filtered(filters)
    favorite_ids: set[UUID] = set()
    if user:
        favorite_ids = await fav_repo.get_favorite_resource_ids(user.id)
    return [_with_is_favorite(r, r.id, favorite_ids) for r in items]


@router.get("/{id}", response_model=ResourceRead)
async def get_resource(
    id: UUID,
    svc: Annotated[ResourceService, Depends(get_resource_service)],
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
    fav_repo: Annotated[FavoriteRepository, Depends(get_favorite_repo)] = ...,
    rating_repo: Annotated[RatingRepository, Depends(get_rating_repo)] = ...,
) -> ResourceRead:
    r = await svc.get_by_id(id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    is_fav = False
    user_rating: int | None = None
    if user:
        is_fav = await fav_repo.has_favorite(user.id, id)
        existing = await rating_repo.get_by_user_and_resource(user.id, id)
        if existing:
            user_rating = existing.score
    return r.model_copy(update={"is_favorite": is_fav, "user_rating": user_rating})


@router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    data: ResourceCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ResourceService, Depends(get_resource_service)],
) -> ResourceRead:
    return await svc.create(user.id, data)


@router.patch("/{id}", response_model=ResourceRead)
async def update_resource(
    id: UUID,
    data: ResourceUpdate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[ResourceService, Depends(get_resource_service)],
) -> ResourceRead:
    r = await svc.update(id, data)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return r
