

from pydantic import BaseModel
from datetime import datetime

from models.types import InterferonUser

from typing import Self

class UserSession(BaseModel):
    intf_user: InterferonUser | None = None
    user_id: str | None = None
    session_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    expiry: datetime | str | float | None = None
    last_active: datetime | str | float | None = None

    @classmethod
    def from_user(cls, user: InterferonUser) -> Self:
        return cls(
            intf_user = user,
            user_id = user.user_id,
            supabase_token = user.supabase_token if user.is_active else None,
            is_active = user.is_active
        )
    
    def to_user(self) -> Self:
        return self.intf_user

    def is_default(self) -> bool:
        return self.model_dump() == UserSession().model_dump()
    
    
