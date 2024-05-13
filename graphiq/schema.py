
# /graphql/schema.py

import strawberry
from strawberry.fastapi import GraphQLRouter
from graphiq.queries import ThreadQuery

@strawberry.type
class Query(ThreadQuery):
    pass

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)


