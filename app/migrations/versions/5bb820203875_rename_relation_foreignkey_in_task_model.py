"""rename relation(ForeignKey) in Task model

Revision ID: 5bb820203875
Revises: 15614b226abd
Create Date: 2024-11-12 19:57:20.249508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bb820203875'
down_revision: Union[str, None] = '15614b226abd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
