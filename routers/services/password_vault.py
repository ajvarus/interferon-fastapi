# /routers/services/password_vault.py

from fastapi import APIRouter, HTTPException, Depends, Security

from dependencies.verify_token import get_verified

from models.types import Passwords
from models.enums import CipherType
from features import PasswordEncryptor


router = APIRouter()

@router.post("/password-vault/")
async def password_vault(ps: Passwords, verified: None = Security(get_verified)):
    try:
        encryptor = PasswordEncryptor()

        if ps.cipher_type == CipherType.ENCRYPT:
            encrypted_passwords = encryptor.encrypt_passwords(ps.passwords)
            return encrypted_passwords
        
        elif ps.cipher_type == CipherType.DECRYPT:
            decrypted_passwords = encryptor.decrypt_passwords(ps.passwords)
            return decrypted_passwords
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))