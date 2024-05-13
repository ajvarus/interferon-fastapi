# /graphiq/types/thread.py

import strawberry

@strawberry.type
class Thread:
    id: strawberry.ID
    title: str
    subtitle: str
    content: str
    user_id: int