# /cypher/encryption/encryption_engine.py


from cryptography.fernet import Fernet




class EncryptionEngine:
    def __init__(self, master_key: str) -> None:
        master_key_bytes = master_key.encode()
        self.fernet = Fernet(master_key_bytes)
    
    def encrypt_text(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt_text(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
    
