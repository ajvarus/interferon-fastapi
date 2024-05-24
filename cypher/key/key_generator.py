# /cypher/key/key_generator.py

from cypher.key.config import APP_SECRET

from cryptography.fernet import Fernet

from typing import Type, TypeVar, Self, Optional

T = TypeVar('T', bound='KeyGenerator')

class KeyGenerator:
    _secret: str = None

    def __new__(cls: Type[T]) -> Type[T]:
        if cls._secret is None:
            cls._secret = APP_SECRET
        return super().__new__(cls)
    
    def __init__(self: T, master_key: Optional[str] = None):
        self.master_key = master_key

    @staticmethod
    def generate_key() -> str:
        key = Fernet.generate_key().decode()
        return key

    @classmethod
    def get_secret(cls) -> str:
        return cls._secret
    
    def get_master_key(self) -> str:
        return self.master_key
    
