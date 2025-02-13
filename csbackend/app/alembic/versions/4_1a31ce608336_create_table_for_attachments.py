"""Create table for conversations

Revision ID: 1a31ce608336
Revises: d98dd8ec85a3
Create Date: 2024-07-31 22:24:34.447891

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

revision = '1a31ce608336'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade():
    # Enable the 'uuid-ossp' extension if not already enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create 'attachments' table with uuid_generate_v4() for generating UUIDs
    op.create_table(
        'attachments',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=func.uuid_generate_v4()),  # UUID primary key with default uuid_generate_v4()
        sa.Column('attachment_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Timestamp for when created
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now())  # Timestamp for when updated
    )

    # Create 'file_attachments' table with uuid_generate_v4() for generating UUIDs and foreign key reference to 'attachments'
    op.create_table(
        'file_attachments',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=func.uuid_generate_v4()),  # UUID primary key with default uuid_generate_v4()
        sa.Column('attachment_id', sa.UUID(), sa.ForeignKey('attachments.id', ondelete='CASCADE')),  # Foreign key reference to 'attachments' table
        sa.Column('storage_type', sa.String(50), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_location', sa.String(512), nullable=True),
        sa.Column('file_data', sa.LargeBinary(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Timestamp for when created
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now())  # Timestamp for when updated
    )

def downgrade():
    # Drop 'file_attachments' and 'attachments' tables if rolling back
    op.drop_table('file_attachments')
    op.drop_table('attachments')
