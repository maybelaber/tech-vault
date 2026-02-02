"""Repository layer (data access)."""

from app.repositories.reference_repo import ReferenceRepository
from app.repositories.user_repo import UserRepository
from app.repositories.resource_repo import ResourceRepository
from app.repositories.rating_repo import RatingRepository
from app.repositories.favorite_repo import FavoriteRepository

__all__ = [
    "ReferenceRepository",
    "UserRepository",
    "ResourceRepository",
    "RatingRepository",
    "FavoriteRepository",
]
