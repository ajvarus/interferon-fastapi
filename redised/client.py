# /redis/

from .config import REDIS_HOST, REDIS_PORT, REDIS_DB
from redis.asyncio import Redis


class RedisManager():

    _client: Redis = None

    @classmethod
    async def init(cls):
        if cls._client is None:
            cls._client = await Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB
            )
            
    @classmethod
    async def get_client(cls) -> Redis:
        if cls._client is None:
            await cls.init()
        return cls._client


