# /cypher/key/key_generator.py

import os

from cryptography.fernet import Fernet

from typing import Optional, Type, TypeVar

T = TypeVar('T', bound='KeyGenerator')

class KeyGenerator:
    _instance: T = None
    _master_key: str = None

    def __new__(cls: Type[T], master_key: Optional[str] = None) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._master_key = master_key if master_key is not None else os.environ.get(
                "APP_SECRET", KeyGenerator.__set_master_key()
            )
        return cls._instance
    
    @staticmethod
    def __set_master_key() -> str:
        key = Fernet.generate_key().decode()
        return key

    @staticmethod
    def generate_key() -> str:
        key = Fernet.generate_key().decode()
        return key

    @classmethod
    def get_master_key(cls) -> str:
        return cls._master_key
    
    