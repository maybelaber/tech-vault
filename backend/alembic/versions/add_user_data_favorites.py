"""add user_data.favorites

Revision ID: add_favorites
Revises: 042b6f6821ea
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "add_favorites"
down_revision: Union[str, None] = "042b6f6821ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorites",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("resource_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["user_data.resources.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_data.users.id"]),
        sa.PrimaryKeyConstraint("user_id", "resource_id"),
        schema="user_data",
    )


def downgrade() -> None:
    op.drop_table("favorites", schema="user_data")
