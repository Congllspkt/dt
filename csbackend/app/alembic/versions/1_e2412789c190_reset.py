"""Initialize models

Revision ID: e2412789c190
Revises:
Create Date: 2023-11-24 22:55:43.195942

"""
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "e2412789c190"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass

def downgrade():
    pass
