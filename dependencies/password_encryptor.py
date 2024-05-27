# /dependencies/password_encryptor.py

from fastapi import Depends, Security
from redis import Redis

from .key_manager import get_key_manager
from .verify_token import get_verified
from .redis import get_redis_client

from cypher.key import KeyManager
from cypher.encryption import EncryptionEngine
from features import PasswordEncryptor

from models.types import UserSession


async def get_password_encryptor(
    session: UserSession = Security(get_verified),
    key_manager: KeyManager = Depends(get_key_manager),
    r: Redis = Depends(get_redis_client),
):
    if not isinstance(session, UserSession):
        session = await get_verified()
    if not isinstance(key_manager, KeyManager):
        key_manager = await get_key_manager()
    if not isinstance(r, Redis):
        r = await get_redis_client()
    encryption_engine = EncryptionEngine()
    return PasswordEncryptor(
        km=key_manager, ee=encryption_engine, user_id=session.user_id, r=r
    )
