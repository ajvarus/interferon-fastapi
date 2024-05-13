# /graphic/queries/thread_queries.py

import strawberry
from typing import Optional, List

from graphiq.types import Thread
from supabased.queries import FetchThreads




@strawberry.type
class Query:
    @strawberry.field
    async def threads(self, user_id: int) -> Optional[List[Thread]]:
        fetcher = FetchThreads()
        response = await fetcher.fetch_threads(user_id)
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