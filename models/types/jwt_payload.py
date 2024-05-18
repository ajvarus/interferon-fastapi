

from pydantic import BaseModel

from .user_session import UserSession

from typing import Self

class JWTPayload(BaseModel):
    sub: str
    exp: int | str
    iat: int | str
    ssn: str

    @classmethod
    async def from_user_session(cls, session: UserSession) -> Self:
        return cls(
            sub=session.user_id,
            ssn=session.session_id,
            iat=int(session.last_active),
            exp=int(session.expiry)
        )