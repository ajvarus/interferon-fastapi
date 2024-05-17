# models/types/auth_request.py

from pydantic import BaseModel

from models.enums import AuthType

class AuthRequest(BaseModel):
    email: str
    password: str
    auth_type: AuthType 