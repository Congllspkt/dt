from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Setting(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    value: Optional[str] = None
    __tablename__ = "settings"
    __table_args__ = {"schema": "admin"}