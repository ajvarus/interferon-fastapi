import strawberry
from strawberry.fastapi import GraphQLRouter

from supabase_client import fetch_user

from typing import Optional, List

@strawberry.type
class Thread:
    id: strawberry.ID
    title: str
    subtitle: str
    content: str
    user_id: int

@strawberry.type
class Query:
    @strawberry.field
    async def threads(self, user_id: int) -> Optional[List[Thread]]:
        response = await fetch_user(user_id)
        threads: list = response.data
        if threads:
            return [Thread(
                id=thread.get("id"),
                title=thread.get("title"),
                subtitle=thread.get("subtitle"),
                content=thread.get("content"),
                user_id=thread.get("user_id")
            ) for thread in threads]
        else:
            return None
        
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)
