import structlog
from typing import Dict

from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from infra.security.auth.password import PasswordHandler
from infra.security.auth.auth_handler import create_access_token
from domain.entities.user import UserEntity
from domain.exceptions.user_exceptions import (
    BadRequestException,
    NotFoundException,
    UserAlreadyExistsException,
)
from presentation.schemas.user import UserRequestDTO


class UserService:

    def __init__(
        self, uow: SQLAlchemyUnitOfWork, logger: structlog.stdlib.BoundLogger
    ) -> None:
        self._uow = uow
        self._logger = logger

    async def create_user(self, user: UserRequestDTO) -> dict:
        self._logger.info("Attempting to create user", extra={"email": user.email})
        hashed_password = PasswordHandler.hash(user.password)

        async with self._uow as uow:
            try:
                existing_user = await uow.user_repository.get_by_email(user.email)
                if existing_user:
                    self._logger.warning(
                        "User already exists", extra={"email": user.email}
                    )
                    raise UserAlreadyExistsException(user.email)

                user_entity = UserEntity(email=user.email, password=hashed_password)
                created_user = await uow.user_repository.create(user_entity)
                await uow.commit()

                self._logger.info(
                    "User created successfully",
                    extra={"email": user.email, "user_id": created_user.id},
                )
                return {
                    "access_token": create_access_token(
                        {"sub": created_user.id, "token_type": "bearer"}
                    )
                }
            except Exception as e:
                await uow.rollback()
                self._logger.error(
                    "Error creating user", extra={"email": user.email, "error": str(e)}
                )
                raise e

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        self._logger.info("Fetching user by email", extra={"email": email})
        async with self._uow as uow:
            try:
                user = await uow.user_repository.get_by_email(email)
                return user
            except Exception as e:
                self._logger.error(
                    "Error fetching user", extra={"email": email, "error": str(e)}
                )
                raise e

    async def login(self, user: UserRequestDTO) -> Dict[str, str]:
        async with self._uow as uow:
            try:
                exist_user = await uow.user_repository.get_by_email(user.email)
                if exist_user is None:
                    self._logger.warning("User not found", extra={"email": user.email})
                    raise NotFoundException(user.email)

                if not PasswordHandler.verify(exist_user.password, user.password):
                    self._logger.warning(
                        "Invalid password", extra={"email": user.email}
                    )
                    raise BadRequestException("Invalid password or email")

                self._logger.info(
                    "User logged in successfully",
                    extra={"email": user.email, "user_id": exist_user.id},
                )
                return {
                    "access_token": create_access_token(
                        {"sub": exist_user.id, "token_type": "bearer"}
                    )
                }
            except Exception as e:
                self._logger.error(
                    "Error logging in", extra={"email": user.email, "error": str(e)}
                )
                raise e
