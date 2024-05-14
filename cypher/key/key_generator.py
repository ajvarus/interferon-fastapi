# /cypher/key/key_generator.py

import secrets

from typing import Optional, Type, TypeVar

T = TypeVar('T', bound='KeyGenerator')

class KeyGenerator:
    _instance: T = None
    _master_key: str = None

    def __new__(cls: Type[T], master_key: Optional[str] = None) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            if master_key is not None:
                cls._master_key = master_key
            elif cls._master_key is None:
                cls._master_key = cls.generate_key()
        
        return cls._instance
    
    @classmethod
    def generate_key(cls) -> str:
        key = secrets.token_hex(16)
        return key

    @classmethod
    def get_master_key(cls) -> str:
        return cls._master_key
    
