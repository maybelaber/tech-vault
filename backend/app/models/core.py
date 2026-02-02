"""
Core (user_data) schema — users, resources (was uploaded_files), ratings (was file_ratings).
SQLAlchemy 2.0 — Mapped[] syntax.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, BigInteger, Numeric, Enum as SQLEnum, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.models.reference import Base as RefBase


# Resource type: Doc, Blueprint, Snippet (was material type / cheat sheets / labs)
import enum


class ResourceType(str, enum.Enum):
    DOC = "doc"
    BLUEPRINT = "blueprint"
    SNIPPET = "snippet"


class Base(RefBase):
    """Inherit same Base so FK to reference schema works."""
    __abstract__ = True


class User(Base):
    """Employees. Links to team and skill_level."""

    __tablename__ = "users"
    __table_args__ = {"schema": "user_data"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    team_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.teams.id"),
        nullable=True,
        index=True,
    )
    skill_level_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.skill_levels.id"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    resources: Mapped[list["Resource"]] = relationship(
        "Resource", back_populates="uploader")
    ratings: Mapped[list["Rating"]] = relationship(
        "Rating", back_populates="user")
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user")


class Resource(Base):
    """Docs / Blueprints / Snippets. Was: uploaded_files."""

    __tablename__ = "resources"
    __table_args__ = {"schema": "user_data"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4)
    uploader_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.users.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    resource_type: Mapped[ResourceType] = mapped_column(
        SQLEnum(ResourceType),
        nullable=False,
        default=ResourceType.DOC,
        index=True,
    )
    technology_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.technologies.id"),
        nullable=True,
        index=True,
    )
    mentor_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.mentors.id"),
        nullable=True,
        index=True,
    )
    team_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.teams.id"),
        nullable=True,
        index=True,
    )
    skill_level_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference.skill_levels.id"),
        nullable=True,
        index=True,
    )
    average_rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2), nullable=False, default=Decimal("0.00")
    )
    ratings_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    uploader: Mapped["User"] = relationship("User", back_populates="resources")
    technology: Mapped["Technology | None"] = relationship(
        "Technology", back_populates="resources", foreign_keys=[technology_id]
    )
    mentor: Mapped["Mentor | None"] = relationship(
        "Mentor", back_populates="resources", foreign_keys=[mentor_id]
    )
    team: Mapped["Team | None"] = relationship(
        "Team", back_populates="resources", foreign_keys=[team_id]
    )
    skill_level: Mapped["SkillLevel | None"] = relationship(
        "SkillLevel", back_populates="resources", foreign_keys=[skill_level_id]
    )
    ratings: Mapped[list["Rating"]] = relationship(
        "Rating", back_populates="resource")
    favorited_by: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="resource")


class Favorite(Base):
    """User favorites (likes). Composite PK (user_id, resource_id)."""

    __tablename__ = "favorites"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "resource_id"),
        {"schema": "user_data"},
    )

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.users.id"),
        nullable=False,
    )
    resource_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.resources.id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    resource: Mapped["Resource"] = relationship(
        "Resource", back_populates="favorited_by"
    )


class Rating(Base):
    """5-star ratings. Was: file_ratings. No deletion allowed per TZ."""

    __tablename__ = "ratings"
    __table_args__ = {"schema": "user_data"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.users.id"),
        nullable=False,
        index=True,
    )
    resource_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.resources.id"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–5
    rating_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="ratings")
    resource: Mapped["Resource"] = relationship(
        "Resource", back_populates="ratings")
