"""Create table for admin preset_messages

Revision ID: d98dd8ec85a3
Revises: 9c0a54914c78
Create Date: 2024-07-19 04:08:04.000976

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

revision = 'd98dd8ec85a3'
down_revision = '9c0a54914c78'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ai_models',
        sa.Column('id', sa.UUID(), primary_key=True, default=sa.text('uuid_generate_v4()')),  # UUID generated using uuid_generate_v4()
        sa.Column('model', sa.String(100), nullable=False, unique = True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('temperature', sa.Float, default=0.7),
        sa.Column('max_tokens', sa.Integer, default=1000),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        schema="admin",
    )


def downgrade():
    op.drop_table('ai_models', schema="admin",)
