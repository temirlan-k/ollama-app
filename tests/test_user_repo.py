import pytest
from infra.db.postgres.repositories.user import UserRepository
from domain.entities.user import UserEntity
from shared import async_session




@pytest.mark.asyncio
async def test_create_user(async_session):
    """Тест создания пользователя в базе."""
    repo = UserRepository(async_session)

    user_entity = UserEntity(email="test@example.com", password="securepassword")
    created_user = await repo.create(user_entity)

    assert created_user is not None
    assert created_user.email == "test@example.com"
    assert created_user.hashed_password == "securepassword"


@pytest.mark.asyncio
async def test_get_user_by_email(async_session):
    """Тест получения пользователя по email."""
    repo = UserRepository(async_session)

    # Создаем пользователя
    user_entity = UserEntity(email="test@example.com", password="securepassword")
    await repo.create(user_entity)

    # Получаем пользователя
    retrieved_user = await repo.get_by_email("test@example.com")

    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.password == "securepassword"


@pytest.mark.asyncio
async def test_get_nonexistent_user_by_email(async_session):
    """Тест получения несуществующего пользователя (должен вернуть None)."""
    repo = UserRepository(async_session)

    user = await repo.get_by_email("notfound@example.com")

    assert user is None
    
