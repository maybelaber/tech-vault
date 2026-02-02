"""add reference.mentors.username (Telegram username for t.me link)

Revision ID: add_mentors_username
Revises: add_favorites
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "add_mentors_username"
down_revision: Union[str, None] = "add_favorites"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "mentors",
        sa.Column("username", sa.String(length=255), nullable=True),
        schema="reference",
    )


def downgrade() -> None:
    op.drop_column("mentors", "username", schema="reference")
