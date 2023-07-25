from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class Stat(BaseModel):
    uid: UUID | None
    email: str
    password: str
    username: str
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True
