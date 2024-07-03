# /models/types/user_session.py

from pydantic import BaseModel
from datetime import datetime

from models.types import InterferonUser

from typing import Union, Self, Dict, Optional, Any


class UserSession(BaseModel):
    intf_user: InterferonUser | None = None
    user_id: str | None = None
    session_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    expiry: datetime | str | float | None = None
    last_active: datetime | str | float | None = None
    error_info: Optional[Dict[str, Any]] = None

    @classmethod
    def from_user(cls, user: InterferonUser) -> Self:
        return cls(
            intf_user=user,
            user_id=user.user_id,
            supabase_token=user.supabase_token if user.is_active else None,
            is_active=user.is_active,
        )

    def to_user(self) -> Union[InterferonUser, None]:
        return self.intf_user

    def is_default(self) -> bool:
        default_session = UserSession()
        result: bool = all(
            getattr(self, field) == getattr(default_session, field)
            for field in self.model_fields
            if field != "error_info"
        )
        return result
        # return self.model_dump() == UserSession().model_dump()
