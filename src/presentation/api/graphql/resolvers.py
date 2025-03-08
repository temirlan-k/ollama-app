import strawberry
from typing import List
import strawberry.types


from application.user_service import UserService
from presentation.api.graphql.schemas import User

@strawberry.type
class Query:
    @strawberry.field
    async def get_all_users(self, info: strawberry.types.Info) -> List[User]:
        user_service: UserService = info.context["user_service"]
        return await user_service.get_all_users()