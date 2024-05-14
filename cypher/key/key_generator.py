# /cypher/key/key_generator.py

from cryptography.fernet import Fernet

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
            else:
                cls._master_key = cls.__set_master_key()
        
        return cls._instance
    
    @classmethod
    def __set_master_key(cls) -> str:
        key = Fernet.generate_key().decode()
        return key

    @classmethod
    def generate_key(cls) -> str:
        key = Fernet.generate_key().decode()
        return key

    @classmethod
    def get_master_key(cls) -> str:
        return cls._master_key
    
    