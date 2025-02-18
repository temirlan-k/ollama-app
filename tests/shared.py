import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from infra.db.postgres.models import Base
from infra.db.postgres.repositories.user import UserRepository
from domain.entities.user import UserEntity


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    """Создает временную in-memory базу данных для тестов."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        yield session

    await engine.dispose()