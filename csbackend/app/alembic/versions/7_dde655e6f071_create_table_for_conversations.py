"""Create table for attachments

Revision ID: 62f56c83e7ff
Revises: fac3a2bffe70
Create Date: 2025-01-15 09:44:32.870508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'dde655e6f071'
down_revision = '62f56c83e7ff'
branch_labels = None
depends_on = None


def upgrade():
    # Create 'conversations' table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(), nullable=False, default=sa.text('uuid_generate_v4()')),  # UUID generated using uuid_generate_v4()
        sa.Column('user_id', UUID(), nullable=True),  # Foreign key to users
        sa.Column('ai_model_id', sa.UUID(), sa.ForeignKey('admin.ai_models.id', ondelete='SET NULL'), nullable=True),  # Foreign key to preset_conversations
        sa.Column('attachment_id', sa.UUID(), sa.ForeignKey('attachments.id', ondelete='CASCADE')),  # Foreign key reference to 'attachments' table
        sa.Column('title', sa.String(255), nullable=True, default='Untitled'),  # Title of the conversation
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),  # Timestamp for when created
        sa.PrimaryKeyConstraint('id'),  # Primary key on 'id'
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')  # Foreign key constraint
    )

    # Create 'messages' table
    op.create_table(
        'messages',
        sa.Column('id', UUID(), nullable=False, default=sa.text('uuid_generate_v4()')),  # UUID generated using uuid_generate_v4()
        sa.Column('conversation_id', UUID(), nullable=True),  # Foreign key to conversations
        sa.Column('sender', sa.String(50), nullable=False),  # Sender of the message
        sa.Column('content', sa.Text(), nullable=False),  # Content of the message
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, default=sa.text('now()')),  # Timestamp for creation
        sa.PrimaryKeyConstraint('id'),  # Primary key on 'id'
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE')  # Foreign key constraint
    )

    # Create 'message_queries' table
    op.create_table(
        'message_queries',
        sa.Column('id', UUID(), nullable=False, default=sa.text('uuid_generate_v4()')),  # UUID generated using uuid_generate_v4()
        sa.Column('message_id', UUID(), nullable=True),  # Foreign key to messages
        sa.Column('prompt', sa.Text(), nullable=False),  # Prompt for the model
        sa.Column('response', sa.Text(), nullable=False),  # Response from the model
        sa.Column('tokens_used', sa.Integer(), nullable=True, default=0),  # Tokens used, default to 0
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, default=sa.text('now()')),  # Timestamp for creation
        sa.PrimaryKeyConstraint('id'),  # Primary key on 'id'
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE')  # Foreign key constraint
    )


def downgrade():
    # Drop the 'message_queries', 'messages', and 'conversations' tables in case of rollback
    op.drop_table('message_queries')
    op.drop_table('messages')
    op.drop_table('conversations')