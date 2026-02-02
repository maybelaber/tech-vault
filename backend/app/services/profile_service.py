"""Profile: user, stats, and mentors."""

from sqlalchemy import select, func

from app.repositories.user_repo import UserRepository
from app.repositories.resource_repo import ResourceRepository
from app.repositories.rating_repo import RatingRepository
from app.repositories.reference_repo import ReferenceRepository
from app.repositories.favorite_repo import FavoriteRepository
from app.models.core import User
from app.schemas.user import UserProfile, UserRead
from app.schemas.profile import MentorRead


class ProfileService:
    def __init__(
        self,
        user_repo: UserRepository,
        resource_repo: ResourceRepository,
        rating_repo: RatingRepository,
        reference_repo: ReferenceRepository,
        favorite_repo: FavoriteRepository,
    ) -> None:
        self._user_repo = user_repo
        self._resource_repo = resource_repo
        self._rating_repo = rating_repo
        self._reference_repo = reference_repo
        self._favorite_repo = favorite_repo

    async def get_profile(self, user: User) -> UserProfile:
        uploaded = await self._resource_repo.count_by_uploader(user.id)
        ratings_count = await self._rating_repo.count_by_user(user.id)
        resources_count = uploaded
        if resources_count == 0:
            fav_ids = await self._favorite_repo.get_favorite_resource_ids(user.id)
            resources_count = len(fav_ids)
        team_count = 12
        if user.team_id:
            session = self._user_repo._session
            result = await session.execute(
                select(func.count()).select_from(User).where(User.team_id == user.team_id)
            )
            team_count = result.scalar() or 12
        favorites = await self._favorite_repo.get_favorites(user.id)
        skills = sorted(
            {r.technology.name for r in favorites if r.technology and r.technology.name},
            key=str.lower,
        )
        # Mentors: from favorites (unique by id) or fallback to all
        seen_mentor_ids = set()
        mentors_from_fav = []
        for r in favorites:
            if r.mentor and r.mentor.id not in seen_mentor_ids:
                seen_mentor_ids.add(r.mentor.id)
                mentors_from_fav.append(r.mentor)
        if mentors_from_fav:
            mentors = [
                MentorRead(
                    id=m.id,
                    name=m.name,
                    role="Mentor",
                    username=getattr(m, "username", None),
                )
                for m in mentors_from_fav
            ]
            mentors_personalized = True
        else:
            mentors_orm = await self._reference_repo.get_mentors()
            mentors = [
                MentorRead(
                    id=m.id,
                    name=m.name,
                    role="Mentor",
                    username=getattr(m, "username", None),
                )
                for m in mentors_orm
            ]
            mentors_personalized = False
        user_read = UserRead.model_validate(user)
        return UserProfile(
            **user_read.model_dump(),
            stats={
                "resources_count": resources_count,
                "ratings_count": ratings_count,
                "team_count": team_count,
            },
            skills=skills,
            mentors=mentors,
            mentors_personalized=mentors_personalized,
        )
