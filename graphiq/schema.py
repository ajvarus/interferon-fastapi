
# /graphql/schema.py

import strawberry
from strawberry.fastapi import GraphQLRouter

from graphiq.queries import ThreadQuery

from graphiq.mutations import StorePasswordsMutation

from graphiq.contexts.passwords_mutation_context import get_graphql_passwords_mutation_context

@strawberry.type
class Query(ThreadQuery):
    pass

@strawberry.type
class Mutation(StorePasswordsMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema=schema, context_getter=get_graphql_passwords_mutation_context)


