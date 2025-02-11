"""Create table for admin ai_models

Revision ID: 62f56c83e7ff
Revises: fac3a2bffe70
Create Date: 2025-01-15 09:44:32.870508

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

revision = '62f56c83e7ff'
down_revision = 'fac3a2bffe70'
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'preset_conversations' table
    op.create_table(
        'preset_conversations',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=func.uuid_generate_v4()),  # UUID primary key
        sa.Column('title', sa.String(255), nullable=False, unique=True),  # Title with unique constraint
        sa.Column('description', sa.Text(), nullable=True),  # Description of the preset conversation
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Created at timestamp
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now()),  # Updated at timestamp
        schema="admin",
    )

    # Create the 'preset_messages' table
    op.create_table(
        'preset_messages',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=func.uuid_generate_v4()),  # UUID primary key
        sa.Column('sequence', sa.Integer(), nullable=False),  # Sequence of the message
        sa.Column('preset_conversation_id', sa.UUID(), sa.ForeignKey('admin.preset_conversations.id', ondelete='CASCADE'), nullable=False),  # Foreign key to preset_conversations
        sa.Column('sender', sa.String(50), nullable=False),  # Sender of the message with varchar(50)
        sa.Column('content', sa.Text(), nullable=True),  # Content of the message
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Created at timestamp
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now()),  # Updated at timestamp
        schema="admin",
    )

def downgrade():
    # Drop the 'preset_messages' and 'preset_conversations' tables in case of rollback
    op.drop_table('preset_messages', schema="admin")
    op.drop_table('preset_conversations', schema="admin")
