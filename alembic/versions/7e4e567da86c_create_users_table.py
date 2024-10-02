"""create users table

Revision ID: 7e4e567da86c
Revises: 
Create Date: 2024-09-26 15:04:34.140128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision: str = '7e4e567da86c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', UUID(as_uuid=True), primary_key=True, default=uuid4(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('users')