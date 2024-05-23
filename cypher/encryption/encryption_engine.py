# /cypher/encryption/encryption_engine.py

from cryptography.fernet import Fernet

from cypher.key import KeyGenerator


class EncryptionEngine:
    def __init__(self, key_generator: KeyGenerator) -> None:
        master_key: str = key_generator.get_master_key()
        master_key_bytes: bytes = master_key.encode()
        self._fernet = Fernet(master_key_bytes)
    
    def encrypt_text(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt_text(self, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode()).decode()
    