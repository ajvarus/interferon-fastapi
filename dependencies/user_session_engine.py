
from fastapi import Depends
from .redis import get_redis_client

from redis.asyncio import Redis

from auth import UserSessionEngine

async def get_user_session_engine(r: Redis = Depends(get_redis_client)) -> UserSessionEngine:
    return UserSessionEngine(r=r)

async def test_get_user_session_engine(r: Redis = None) -> UserSessionEngine:
    r = await get_redis_client()
    return UserSessionEngine(r=r)