"""Create table for users

Revision ID: 9c0a54914c78
Revises: e2412789c190
Create Date: 2024-06-17 14:42:44.639457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

revision = '9c0a54914c78'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
        # Create 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=func.uuid_generate_v4()),  # UUID for user ID
        sa.Column('email', sa.String(255), nullable=False),  # Email
        sa.Column('is_active', sa.Boolean(), nullable=False),  # Is active field
        sa.Column('is_superuser', sa.Boolean(), nullable=False),  # Superuser flag
        sa.Column('full_name', sa.String(255), nullable=True),  # Full name (nullable)
        sa.Column('hashed_password', sa.String(), nullable=False),  # Hashed password (non-nullable)
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Timestamp for when created
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(),),  # Timestamp for when created
    )

    # Create unique index for 'email'
    op.create_index('users_email_idx', 'users', ['email'], unique=True)

    # Create 'items' table
    op.create_table(
        'items',
        sa.Column('id', UUID(), nullable=False),  # UUID for item ID
        sa.Column('owner_id', UUID(), nullable=False),  # UUID for owner (foreign key)
        sa.Column('title', sa.String(255), nullable=False),  # Item title (non-nullable)
        sa.Column('description', sa.String(255), nullable=True),  # Item description (nullable)
        sa.PrimaryKeyConstraint('id'),  # Primary key on 'id'
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE')  # Foreign key linking to 'users'
    )

def downgrade():
    op.drop_index(op.f("users_email_idx"), table_name="users")
    op.drop_table("users")
    op.drop_table("items")
