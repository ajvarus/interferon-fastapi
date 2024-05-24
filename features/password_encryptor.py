from cypher.encryption import EncryptionEngine
from cypher.key import KeyGenerator

from cypher.key import KeyManager


from typing import Dict

class PasswordEncryptor:
    def __init__(self, km: KeyManager, ee: EncryptionEngine, user_id: str) -> None:
        self.user_id = user_id
        self.km = km
        self.ee = ee
        self.encryptor = None

    async def _initialise(self) -> None:
        key = await self.km.retrieve_key(self.user_id)
        self.encryptor: EncryptionEngine = self.ee.init(key)

    async def encrypt_passwords(self, passwords: Dict[str, str]) -> Dict[str, str]:
        if self.encryptor is None:
            await self._initialise()
        encrypted_passwords: Dict[str, str] = {}
        if passwords:
            for name, password in passwords.items():
                encrypted_password = self.encryptor.encrypt_text(password)
                encrypted_passwords[name] = encrypted_password
        return encrypted_passwords
    
    async def decrypt_passwords(self, passwords: Dict[str, str]) -> Dict[str, str]:
        if self.encryptor is None:
            await self._initialise()
        decrypted_passwords: Dict[str, str] = {}
        if passwords:
            for name, password in passwords.items():
                decrypted_password = self.encryptor.decrypt_text(password)
                decrypted_passwords[name] = decrypted_password
        return decrypted_passwords
    
