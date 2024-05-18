
from pydantic import BaseModel

from .auth_request import AuthRequest

from typing import Self

class SignUpCredentials(BaseModel):
    email: str
    password: str

    @classmethod
    def from_auth_request(cls, auth_request: AuthRequest) -> Self:
        return cls(email=auth_request.email, password=auth_request.password)

