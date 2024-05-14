from cypher.encryption import EncryptionEngine
from cypher.key import KeyGenerator


from typing import Dict

class PasswordEncryptor:
    def __init__(self) -> None:
        key_generator = KeyGenerator()
        self.__encryptor = EncryptionEngine(key_generator.get_master_key())

    def encrypt_passwords(self, passwords: Dict[str, str]) -> Dict[str, str]:
        if not passwords:
            raise ValueError("No passwords provided for encryption.")

        encrypted_passwords: Dict[str, str] = {}
        for name, password in passwords.items():
            encrypted_password = self.__encryptor.encrypt_text(password)
            encrypted_passwords[name] = encrypted_password

        return encrypted_passwords
    
    def decrypt_passwords(self, passwords: Dict[str, str]) -> Dict[str, str]:
        if not passwords:
            raise ValueError("No passwords provided for encryption.")

        decrypted_passwords: Dict[str, str] = {}
        for name, password in passwords.items():
            decrypted_password = self.__encryptor.decrypt_text(password)
            decrypted_passwords[name] = decrypted_password

        return decrypted_passwords
    
