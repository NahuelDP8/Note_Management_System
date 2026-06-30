"""add user-owned categories

Revision ID: 8b8d5f6a2c1e
Revises: c48e072342ba
Create Date: 2026-06-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b8d5f6a2c1e"
down_revision: Union[str, None] = "c48e072342ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("categories", sa.Column("user_id", sa.Integer(), nullable=True))
    op.drop_constraint("categories_name_key", "categories", type_="unique")
    op.create_foreign_key(
        "fk_categories_user_id_users",
        "categories",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_categories_global_name_lower_unique",
        "categories",
        [sa.text("lower(name)")],
        unique=True,
        postgresql_where=sa.text("user_id IS NULL"),
    )
    op.create_index(
        "ix_categories_user_name_lower_unique",
        "categories",
        ["user_id", sa.text("lower(name)")],
        unique=True,
        postgresql_where=sa.text("user_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_categories_user_name_lower_unique", table_name="categories")
    op.drop_index("ix_categories_global_name_lower_unique", table_name="categories")
    op.drop_constraint("fk_categories_user_id_users", "categories", type_="foreignkey")
    op.create_unique_constraint("categories_name_key", "categories", ["name"])
    op.drop_column("categories", "user_id")
