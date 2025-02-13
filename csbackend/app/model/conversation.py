from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Conversation(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    attachment_id: UUID = Field(foreign_key="attachments.id", nullable=False)
    title: str = Field(default="Untitled", max_length=255)
    __tablename__ = "conversations"