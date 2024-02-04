"""add content coumn to posts table

Revision ID: 6af9c842405a
Revises: 4b5d4a9a1338
Create Date: 2024-02-04 18:44:59.954076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6af9c842405a'
down_revision: Union[str, None] = '4b5d4a9a1338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", 'content')
    pass
