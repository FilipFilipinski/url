from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class Stat(BaseModel):
    l_uid: UUID | None
    link_uid: UUID
    date: datetime = Field(default_factory=datetime.now)
    views: int

    class Config:
        validate_assignment = True
