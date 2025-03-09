from fastapi import Depends, Request
import strawberry
from strawberry.fastapi import GraphQLRouter

from presentation.api.graphql.resolvers import Query,Mutation
from infra.security.auth.jwt_bearer import JWTBearer
from bootstrap.di_container import container


async def get_context(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]
        try:
            jwt_bearer = JWTBearer()
            current_user = await jwt_bearer(request)
        except:
            current_user = None
    else:
        current_user = None
    return {
        "user_service": container.user_service(),
        "current_user": current_user,
        "request": request
    }

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context, dependencies=[Depends(get_context)])
