from cypher.encryption import EncryptionEngine

from cypher.key import KeyManager

from graphiq.types import PasswordInput, PasswordRequest, PasswordFetchResponse

from typing import Dict, List


class PasswordEncryptor:
    def __init__(self, km: KeyManager, ee: EncryptionEngine, user_id: str) -> None:
        self.user_id = user_id
        self.km = km
        self.ee = ee
        self.encryptor = None

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
                p: dict = p.get("node")
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
