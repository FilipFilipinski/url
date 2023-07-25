from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class Link(BaseModel):
    l_id: UUID | None
    owner_uid: UUID
    original_link: str
    short_link: str
    protected: bool
    password: str | None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True
