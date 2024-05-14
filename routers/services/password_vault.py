# /routers/services/encrypt_passwords.py

from fastapi import APIRouter, HTTPException

from models import Passwords
from features import PasswordEncryptor


router = APIRouter()

@router.post("/password-vault/")
def password_vault(request: Passwords):
    try:
        encryptor = PasswordEncryptor()
        encrypted_passwords = encryptor.encrypt_passwords(request.passwords)
        return encrypted_passwords
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))