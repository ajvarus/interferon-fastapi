# /cypher/key/key_manager.py

from typing import Self

from supabase._async.client import AsyncClient as SupabaseClient
from redis import Redis

from cypher.key import KeyGenerator
from cypher.encryption import EncryptionEngine

from supabased.migrations.auth import InsertUserKey
from supabased.queries.auth import FetchUserKey

from models.types import InterferonUser, UserSession

class KeyManager:
    def __init__(
            self, 
            ik: InsertUserKey, 
            fk: FetchUserKey,
            r: Redis,
            kg: KeyGenerator,
            ee: EncryptionEngine
            ) -> None:
        self._ik = ik
        self._fk = fk
        self._r = r
        self._kg = kg
        self._ee = ee.init(kg.get_secret())

    async def manage_key_for(self: Self, user: InterferonUser) -> None:
        try:
            if user.is_active:
                if user.is_new:
                    key = self._kg.generate_key()
                    encrypted_key = self._ee.encrypt_text(plaintext=key)
                    is_inserted: bool = await self._ik.insert_user_key(user.user_id, encrypted_key)
                    if is_inserted:
                        await self._r.set(f"{user.user_id}:master_key", encrypted_key)
                    else:
                        raise Exception()
                elif user.is_new == False:
                    master_key_exists: bool = (await self._r.exists(f"{user.user_id}:master_key")) > 0
                    if not master_key_exists:
                        row: dict = await self._fk.fetch_user_key(user.user_id)
                        if row:
                            encrypted_key: str = row.get("master_key", None)
                            if encrypted_key:
                                await self._r.set(f"{user.user_id}:master_key", encrypted_key)
            elif user.is_active == False:
                master_key_exists: bool = True if await self._r.exists(f"{user.user_id}:master_key") else False
                if master_key_exists:
                    await self._r.delete(f"{user.user_id}:master_key")
            else: 
                raise Exception("Key management failure!")
        except Exception as e:
            print(str(e))
            raise

    async def retrieve_key(self, user_id: str) -> str:
        key_name: str = f"{user_id}:master_key"
        key: str = ""
        try:
            if (await self._r.exists(key_name)) > 0:
                encrypted_key_bytes: bytes = await self._r.get(key_name)
                encrypted_key: str = encrypted_key_bytes.decode()
                key = self._ee.decrypt_text(encrypted_key)
                return key
            else:
                raise Exception("Failed to retrieve key.")
        except Exception as e:
            return key


# The below function is a wrapper for key-manager
# used in AuthSessionInterface 
from functools import wraps
from typing import Any, Callable

def manageuserkey(get_key_manager):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            session: UserSession = await func(*args, **kwargs)
            if not session.is_default(): 
                user: InterferonUser = session.to_user()
                key_manager: KeyManager = await get_key_manager()
                await key_manager.manage_key_for(user)
            return session
        return wrapper
    return decorator