import strawberry
from datetime import datetime

@strawberry.type
class User:
    id: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


@strawberry.type
class Token:
    access_token: str
