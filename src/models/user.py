from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    uid: UUID | None
    admin: bool = False
    email: str
    password: str = Field(exclude=True)
    username: str
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True
