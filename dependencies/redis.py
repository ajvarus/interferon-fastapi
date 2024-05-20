
from redis.asyncio import Redis
from redised import RedisManager

async def get_redis_client() -> Redis:
    return await RedisManager.get_client()
