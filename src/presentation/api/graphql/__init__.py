import strawberry
from presentation.api.graphql.resolvers import Query
from strawberry.fastapi import GraphQLRouter
from bootstrap.di_container import container

def get_context():
    return {
        "user_service": container.user_service()
    }


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema,context_getter=get_context)
