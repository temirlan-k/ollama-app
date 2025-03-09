import strawberry
from typing import List

import strawberry.types

from application.user_service import UserService
from presentation.api.graphql.schemas import Token, User
from presentation.schemas.user import UserRequestDTO
from domain.exceptions.user_exceptions import (
    BadRequestException,
    NotFoundException,
    UserAlreadyExistsException,
)


@strawberry.type
class Query:

    @strawberry.field
    async def get_all_users(self, info: strawberry.types.Info)-> List[User]:
        user_service: UserService = info.context["user_service"]
        return await user_service.get_all_users()
    
@strawberry.type
class Mutation:

    @strawberry.mutation
    async def register(self,email: str, password: str, info: strawberry.types.Info)-> Token:
        user_service: UserService = info.context["user_service"]
        req_dto = UserRequestDTO(email=email, password=password)
        try:
            user_token = await user_service.create_user(req_dto)
            return Token(access_token=user_token.get('access_token'))
        except UserAlreadyExistsException as e:
            raise ValueError(str(e.message))
        

    @strawberry.mutation
    async def login(self,email: str, password: str, info: strawberry.types.Info)-> Token:
        user_service: UserService = info.context["user_service"]
        req_dto = UserRequestDTO(email=email, password=password)
        try:
            user_token = await user_service.login(req_dto)
            return Token(access_token=user_token.get('access_token'))
        except NotFoundException as e:
            raise ValueError(e.message)
        except BadRequestException as e:
            raise ValueError(e.message)

        