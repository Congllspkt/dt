from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional

class MessageQuery(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    message_id: UUID = Field(foreign_key="messages.id", nullable=False)
    prompt: str
    response: str
    model_name: str
    tokens_used: int
    __tablename__ = "message_queries"
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

