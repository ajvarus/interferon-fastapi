# /graphql/schema.py

import strawberry
from strawberry.fastapi import GraphQLRouter

from graphiq.queries import ThreadQuery
from graphiq.queries import FetchPasswordsQuery

from graphiq.mutations import StorePasswordsMutation
from graphiq.mutations import UpdatePasswordsMutation
from graphiq.mutations import DeletePasswordsMutation

from graphiq.contexts.graphql_context import get_graphql_context


@strawberry.type
class Query(ThreadQuery, FetchPasswordsQuery):
    pass


@strawberry.type
class Mutation(
    StorePasswordsMutation, UpdatePasswordsMutation, DeletePasswordsMutation
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema=schema, context_getter=get_graphql_context)
