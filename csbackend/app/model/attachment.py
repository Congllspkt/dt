from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Attachment(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    attachment_name: str
    description: Optional[str] = None
    __tablename__ = "attachments"