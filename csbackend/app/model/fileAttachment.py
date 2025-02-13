from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class FileAttachment(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    attachment_id: UUID = Field(foreign_key="attachments.id", nullable=False)
    storage_type: str
    file_name: str
    file_type: str
    file_size: int
    file_location: Optional[str] = None
    file_data: Optional[bytes] = None
    __tablename__ = "file_attachments"