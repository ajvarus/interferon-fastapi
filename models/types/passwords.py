# models/types/password.py

from pydantic import BaseModel
from typing import Dict

from models.enums import CipherType

class Passwords(BaseModel):
    passwords: Dict[str, str]
    cipher_type: CipherType 
