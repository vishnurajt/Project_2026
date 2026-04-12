"""add phone number

Revision ID: 4eceb980d811
Revises: 
Create Date: 2026-04-12 14:38:45.519973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4eceb980d811'
down_revision: Union[str, None] = '4726eb8098b8'  # ← points to initial tables
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass