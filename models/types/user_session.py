

from pydantic import BaseModel
from datetime import datetime

from models.types import InterferonUser

from typing import Self

class UserSession(BaseModel):
    user_id: str | None = None
    session_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    expiry: datetime | str | float | None = None
    last_active: datetime | str | float | None = None

    @classmethod
    async def from_user(cls, user: InterferonUser) -> Self:
        return cls(
            user_id = user.user_id,
            supabase_token = user.supabase_token
        )

    def is_default(self) -> bool:
        return self.model_dump() == UserSession().model_dump()
    
    
