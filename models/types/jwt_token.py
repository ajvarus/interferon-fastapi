

from pydantic import BaseModel


class JWTToken(BaseModel):
    sub: str
    exp: int | str
    iat: int | str
