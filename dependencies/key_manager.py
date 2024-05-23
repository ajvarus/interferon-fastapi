
from supabased.migrations.auth import InsertUserKey
from supabased.queries.auth import FetchUserKey
from .user_key import get_insert_user_key, get_fetch_user_key

from cypher.key import KeyGenerator, KeyManager
from cypher.encryption import EncryptionEngine

from redis import Redis
from .redis import get_redis_client


async def get_key_manager(
        user_key_inserter: InsertUserKey = None,
        user_key_fetcher: FetchUserKey = None,
        r: Redis = None,
        key_generator: KeyGenerator = None,
        encryption_engine: EncryptionEngine = None
) -> KeyManager:
    if user_key_inserter is None:
        user_key_inserter = await get_insert_user_key()
    if user_key_fetcher is None:
        user_key_fetcher = await get_fetch_user_key()
    if r is None:
        r = await get_redis_client()
    if key_generator is None:
        key_generator = KeyGenerator()
    if encryption_engine is None:
        encryption_engine = EncryptionEngine(key_generator)
    return KeyManager(
        ik=user_key_inserter,
        fk=user_key_fetcher,
        kg=key_generator,
        ee=encryption_engine,
        r=r
    )