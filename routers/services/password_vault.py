# /routers/services/password_vault.py

from fastapi import APIRouter, HTTPException

from models.types import Passwords
from models.enums import CipherType
from features import PasswordEncryptor


router = APIRouter()

@router.post("/password-vault/")
def password_vault(request: Passwords):
    try:
        encryptor = PasswordEncryptor()

        if request.cipher_type == CipherType.ENCRYPT:
            encrypted_passwords = encryptor.encrypt_passwords(request.passwords)
            return encrypted_passwords
        
        elif request.cipher_type == CipherType.DECRYPT:
            decrypted_passwords = encryptor.decrypt_passwords(request.passwords)
            return decrypted_passwords
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))