"""
Reference (read-only) schema — adapted from hm_data.
Domain: Technologies, Mentors, Teams, Skill Levels.
SQLAlchemy 2.0 — Mapped[] syntax.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base for all models."""


class Technology(Base):
    """Technologies (e.g. Python, Kubernetes, Figma). Was: subjects."""

    __tablename__ = "technologies"
    __table_args__ = {"schema": "reference"}

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # relationships (for ORM; core.resources references this)
    resources: Mapped[list["Resource"]] = relationship(
        "Resource",
        back_populates="technology",
        foreign_keys="Resource.technology_id",
    )


class Mentor(Base):
    """Mentors / Tech Leads. Was: teachers."""

    __tablename__ = "mentors"
    __table_args__ = {"schema": "reference"}

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Telegram username for t.me link
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    resources: Mapped[list["Resource"]] = relationship(
        "Resource",
        back_populates="mentor",
        foreign_keys="Resource.mentor_id",
    )


class Team(Base):
    """Teams. Was: groups."""

    __tablename__ = "teams"
    __table_args__ = {"schema": "reference"}

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    resources: Mapped[list["Resource"]] = relationship(
        "Resource",
        back_populates="team",
        foreign_keys="Resource.team_id",
    )


class SkillLevel(Base):
    """Skill levels (Junior, Middle, Senior). Was: semesters."""

    __tablename__ = "skill_levels"
    __table_args__ = {"schema": "reference"}

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)  # Junior, Middle, Senior
    sort_order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    resources: Mapped[list["Resource"]] = relationship(
        "Resource",
        back_populates="skill_level",
        foreign_keys="Resource.skill_level_id",
    )
