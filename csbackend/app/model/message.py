from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional

class Message(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    sender: str
    content: str
    __tablename__ = "messages"
