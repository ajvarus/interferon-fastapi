

from pydantic import BaseModel

from .user_session import UserSession

from typing import Self

class JWTPayload(BaseModel):
    sub: str | None = None
    exp: int | str | None = None
    iat: int | str | None = None
    ssn: str | None = None

    @classmethod
    async def from_user_session(cls, session: UserSession) -> Self:
        return cls(
            sub=session.user_id,
            ssn=session.session_id,
            iat=int(session.last_active),
            exp=int(session.expiry)
        )
    
    def is_default(self) -> bool:
        return self.model_dump() == JWTPayload().model_dump()