

from pydantic import BaseModel
from datetime import datetime
from typing import Self


class InterferonUser(BaseModel):
    user_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    is_new: bool | None = None
    last_active: datetime | str | None = None

    def is_default(self) -> bool:
        return self.model_dump() == InterferonUser().model_dump()
    
    def transfer_non_none_values_from(self, user: Self) -> None:
        for key, value in user.model_dump().items():
            if value is not None:
                setattr(self, key, value)