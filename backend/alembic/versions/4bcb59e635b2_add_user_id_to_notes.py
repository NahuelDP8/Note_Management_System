"""add user_id to notes

Revision ID: 4bcb59e635b2
Revises: 0e62083203f5
Create Date: 2026-02-10 17:58:41.373836
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '4bcb59e635b2'
down_revision: Union[str, None] = '0e62083203f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'notes',
        sa.Column('user_id', sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('notes', 'user_id')
