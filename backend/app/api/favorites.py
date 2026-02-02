"""User favorites (likes): toggle and list."""

from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.dependencies import get_favorite_repo, get_resource_repo
from app.models.core import User
from app.repositories.favorite_repo import FavoriteRepository
from app.repositories.resource_repo import ResourceRepository
from app.schemas.resource import ResourceRead

router = APIRouter(tags=["favorites"])


@router.get("/favorites", response_model=list[ResourceRead])
async def list_favorites(
    user: Annotated[User, Depends(get_current_user)],
    fav_repo: Annotated[FavoriteRepository, Depends(get_favorite_repo)],
) -> list[ResourceRead]:
    """Return resources favorited by the current user."""
    resources = await fav_repo.get_favorites(user.id)
    return [ResourceRead.model_validate(r).model_copy(update={"is_favorite": True}) for r in resources]


@router.post("/resources/{resource_id}/favorite")
async def toggle_favorite(
    resource_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    fav_repo: Annotated[FavoriteRepository, Depends(get_favorite_repo)],
    resource_repo: Annotated[ResourceRepository, Depends(get_resource_repo)],
) -> dict[str, bool]:
    """Toggle like for a resource. Returns new state: { \"is_favorite\": true|false }."""
    resource = await resource_repo.get_by_id(resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    is_favorite = await fav_repo.toggle_favorite(user.id, resource_id)
    return {"is_favorite": is_favorite}
