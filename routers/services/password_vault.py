# /routers/services/password_vault.py

from fastapi import APIRouter, HTTPException, Depends, Security

from dependencies.verify_token import get_verified
from dependencies.password_encryptor import get_password_encryptor

from models.types import Passwords
from models.enums import CipherType
from features import PasswordEncryptor

from typing import Dict

router = APIRouter()

@router.post("/password-vault/")
async def password_vault(ps: Passwords, encryptor: PasswordEncryptor = Depends(get_password_encryptor)) -> Dict[str, str]:
    try:
        if ps.cipher_type == CipherType.ENCRYPT:
            encrypted_passwords: Dict[str, str] = await encryptor.encrypt_passwords(ps.passwords)
            return encrypted_passwords
        
        elif ps.cipher_type == CipherType.DECRYPT:
            decrypted_passwords = await encryptor.decrypt_passwords(ps.passwords)
            return decrypted_passwords
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))