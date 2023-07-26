from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models.user import User


class AccessToken(BaseModel):
    token: UUID = Field(default_factory=uuid4)
    user: User

    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True
