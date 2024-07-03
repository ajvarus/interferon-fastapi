from fastapi import Depends

from supabased.migrations.auth import InsertUserKey
from supabased.queries.auth import FetchUserKey
from .user_key import get_insert_user_key, get_fetch_user_key

from cypher.key import KeyGenerator, KeyManager
from cypher.encryption import EncryptionEngine

from redis import Redis
from .redis import get_redis_client


async def get_key_manager(
    user_key_inserter: InsertUserKey = Depends(get_insert_user_key),
    user_key_fetcher: FetchUserKey = Depends(get_fetch_user_key),
    r: Redis = Depends(get_redis_client),
) -> KeyManager:
    if not isinstance(user_key_inserter, InsertUserKey):
        user_key_inserter = await get_insert_user_key()
    if not isinstance(user_key_fetcher, FetchUserKey):
        user_key_fetcher = await get_fetch_user_key()
    if not isinstance(r, Redis):
        r = await get_redis_client()
    key_generator = KeyGenerator()
    encryption_engine = EncryptionEngine()
    return KeyManager(
        ik=user_key_inserter,
        fk=user_key_fetcher,
        kg=key_generator,
        ee=encryption_engine,
        r=r,
    )
