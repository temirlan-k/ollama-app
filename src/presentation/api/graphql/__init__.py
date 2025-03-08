import strawberry
from presentation.api.graphql.resolvers import Query
from strawberry.fastapi import GraphQLRouter


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
