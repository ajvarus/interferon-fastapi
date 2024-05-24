# /dependencies/password_encryptor.py

from fastapi import Depends, Security

from .key_manager import get_key_manager
from .verify_token import get_verified

from cypher.key import KeyManager
from cypher.encryption import EncryptionEngine
from features import PasswordEncryptor

from models.types import UserSession

async def get_password_encryptor(
        session: UserSession = Security(get_verified),
        key_manager: KeyManager = Depends(get_key_manager)
):
    encryption_engine = EncryptionEngine()
    return PasswordEncryptor(
        km=key_manager,
        ee=encryption_engine,
        user_id=session.user_id
    )