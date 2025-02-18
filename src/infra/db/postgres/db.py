from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres", echo=False
)


async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
