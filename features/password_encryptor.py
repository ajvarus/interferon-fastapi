from cypher.encryption import EncryptionEngine

from cypher.key import KeyManager

from graphiq.types import (
    PasswordInput,
    PasswordRequest,
    PasswordFetchResponse,
    PasswordCacheResponse,
)

from typing import Dict, List

from redis import Redis

from models.enums import OpType


class PasswordEncryptor:
    def __init__(
        self, km: KeyManager, ee: EncryptionEngine, user_id: str, r: Redis
    ) -> None:
        self.user_id = user_id
        self.km = km
        self.ee = ee
        self.encryptor = None
        self.r = r

    async def _initialise(self) -> None:
        key = await self.km.retrieve_key(self.user_id)
        self.encryptor: EncryptionEngine = self.ee.init(key)

    async def encrypt_passwords(
        self, passwords: List[PasswordInput]
    ) -> List[PasswordRequest]:
        if self.encryptor is None:
            await self._initialise()
        encrypted_passwords: List[PasswordRequest] = []
        if passwords:
            for p in passwords:
                encrypted_password: str = self.encryptor.encrypt_text(p.password)
                encrypted_passwords.append(
                    PasswordRequest(
                        user_id=self.user_id,
                        password_name=p.password_name,
                        encrypted_password=encrypted_password,
                    )
                )
        return encrypted_passwords

    async def decrypt_passwords(
        self, passwords: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        if self.encryptor is None:
            await self._initialise()
        decrypted_passwords: List[Dict[str, str]] = []
        if passwords:
            for p in passwords:
                decrypted_password: str = self.encryptor.decrypt_text(
                    p.get("encrypted_password")
                )
                decrypted_passwords.append(
                    PasswordFetchResponse(
                        id=p.get("id"),
                        password_name=p.get("password_name"),
                        decrypted_password=decrypted_password,
                    )
                )
        return decrypted_passwords

    async def decrypt_single_password(self, password: str) -> str:
        if self.encryptor is None:
            await self._initialise()
        if password:
            decrypted_password: str = self.encryptor.decrypt_text(password)
        return decrypted_password

    async def cache_passwords(self, passwords: List[Dict], op_type: OpType) -> bool:
        redis_key: str = f"{self.user_id}:passwords"
        cache_exists = await self.r.exists(redis_key) == 1
        if cache_exists:
            if op_type == OpType.ADD:
                is_added: bool = await self.add_to_cache(passwords, redis_key)
                return is_added
        else:
            if op_type == OpType.WRITE:
                is_written: bool = await self.write_to_cache(passwords, redis_key)
                return is_written

    async def add_to_cache(self, passwords: List[Dict], key: str) -> bool:
        try:
            existing_passwords = await self.r.hkeys(key)
            new_passwords = []
            for p in passwords:
                if p["id"] not in existing_passwords:
                    new_passwords.append(p)
            if new_passwords:
                password_mapping = {
                    p["id"]: p["encrypted_password"] for p in new_passwords
                }
                await self.r.hset(key, mapping=password_mapping)
            return True
        except Exception as e:
            return False

    async def write_to_cache(self, passwords: List[Dict], key: str) -> bool:
        try:
            await self.r.delete(key)
            password_mapping = {
                p.get("id"): p.get("encrypted_password") for p in passwords
            }
            await self.r.hset(key, mapping=password_mapping)
            return True
        except Exception as e:
            return False

    async def retrieve_passwords_from_cache(
        self, password_ids: List[str]
    ) -> List[Dict[str, str]]:
        redis_key: str = f"{self.user_id}:passwords"
        try:
            encrypted_passwords: List[bytes] = await self.r.hmget(
                redis_key, *password_ids
            )
            decrypted_passwords: List[PasswordCacheResponse] = [
                PasswordCacheResponse(
                    id=password_id,
                    decrypted_password=await self.decrypt_single_password(
                        encrypted_password.decode()
                    ),
                )
                for password_id, encrypted_password in zip(
                    password_ids, encrypted_passwords
                )
            ]
            return decrypted_passwords
        except Exception as e:
            return []
