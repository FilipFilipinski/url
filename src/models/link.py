from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Link(BaseModel):
    l_uid: UUID | None
    owner_uid: UUID
    original_link: str
    short_link: str
    protected: bool
    password: str | None = Field(exclude=True)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True
