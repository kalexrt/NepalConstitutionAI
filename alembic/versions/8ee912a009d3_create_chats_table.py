"""create chats table

Revision ID: 8ee912a009d3
Revises: 7e4e567da86c
Create Date: 2024-09-26 15:09:53.470104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision: str = '8ee912a009d3'
down_revision: Union[str, None] = '7e4e567da86c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create chat_session table
    op.create_table(
        'chat_session',
        sa.Column('chat_session_id', UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False),
        sa.Column('chat_date', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column('modified_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column('created_by', UUID(as_uuid=True), sa.ForeignKey('users.user_id'), nullable=False)
    )

    # Create chat_message table
    op.create_table(
        'chat_message',
        sa.Column('chat_message_id', UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False),
        sa.Column('message_by', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('message_time', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Column('chat_session_id', UUID(as_uuid=True), sa.ForeignKey('chat_session.chat_session_id'), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('chat_message')
    op.drop_table('chat_session')
