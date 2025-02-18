from datetime import datetime
from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int | None = None
    email: str
    password: str | None = None
    created_at: datetime | None = datetime.now()
    updated_at: datetime | None = datetime.now()

    class Config:
        from_attributes = True
