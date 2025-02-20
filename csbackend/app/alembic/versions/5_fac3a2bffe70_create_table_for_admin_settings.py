"""Create table for admin settings

Revision ID: fac3a2bffe70
Revises: 1a31ce608336
Create Date: 2025-01-15 09:31:51.387952

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision = 'fac3a2bffe70'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'settings',
        sa.Column('id', UUID(), nullable=False, default=sa.text('uuid_generate_v4()')),  # UUID generated using uuid_generate_v4()
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Timestamp for when created
        schema="admin",
    )

def downgrade():
    op.drop_table('settings', schema="admin")
