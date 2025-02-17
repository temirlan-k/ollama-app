from sqlalchemy.ext.asyncio import AsyncSession
from infra.db.postgres.repositories.request import RequestRepository
from infra.db.postgres.repositories.user import UserRepository

class SQLAlchemyUnitOfWork:

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user_repository = UserRepository(self.session)
        self.request_repository = RequestRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

