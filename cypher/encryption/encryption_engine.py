# /cypher/encryption/encryption_engine.py

from cryptography.fernet import Fernet

from typing import Self

class EncryptionEngine:
    def __init__(self) -> None:
        self._fernet = None

    def init(self, key: str) -> Self:
        key_in_bytes: bytes = key.encode()
        self._fernet = Fernet(key_in_bytes)
        return self
    
    def encrypt_text(self, plaintext: str) -> str:
        if self._fernet:
            return self._fernet.encrypt(plaintext.encode()).decode()
        raise

    def decrypt_text(self, ciphertext: str) -> str:
        if self._fernet:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        raise
    