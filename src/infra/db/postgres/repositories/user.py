from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user import UserEntity
from infra.db.postgres.models.user import User

class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: UserEntity)-> UserEntity:
        user_db = User(
            email=user.email,
            hashed_password=user.password
        )
        self._session.add(user_db)
        await self._session.flush()
        return user_db


    async def get_by_email(self, email: str)-> UserEntity | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        user_db = result.scalars().first()
        return UserEntity(id=user_db.id, email=user_db.email, created_at=user_db.created_at) if user_db else None


