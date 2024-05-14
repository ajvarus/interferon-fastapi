# /cypher/encryption/encryption_engine.py

import base64
from cryptography.fernet import Fernet

import secrets


class EncryptionEngine:
    def __init__(self, master_key: str) -> None:
        master_key_bytes = master_key.encode()
        master_key_b64 = base64.urlsafe_b64encode(master_key_bytes)
        self.fernet = Fernet(master_key_b64)
    
    def encrypt_text(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt_text(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
    
