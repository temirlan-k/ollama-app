

from domain.exceptions.user_exceptions import UserAlreadyExistsException
from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from infra.security.auth.password import hash_password, verify_password
from domain.entities.user import UserEntity
from presentation.schemas.user import UserRequestDTO
from infra.security.auth.auth_handler import create_access_token

class UserService:

    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self._uow = uow

    async def create_user(self, user: UserRequestDTO) -> dict:
        hashed_password = hash_password(user.password)
        async with self._uow as uow:
            try:
                existing_user = await uow.user_repository.get_by_email(user.email)
                if existing_user:
                    raise UserAlreadyExistsException(user.email)
                user = UserEntity(email=user.email,password=hashed_password)
                created_user = await uow.user_repository.create(user)
                await uow.commit()
                return {"access_token": create_access_token({"sub": (created_user.id), "token_type": "bearer" })}
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        async with self._uow as uow:
            return await uow.user_repository.get_by_email(email)
        