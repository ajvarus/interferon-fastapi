from pydantic import BaseModel
from typing import Optional


class SupabaseUser(BaseModel):
    user: Optional[dict] = {}
    session: Optional[dict] = {}
    # error_code: Optional[int] = None

    def is_default(self):
        return self.model_dump() == SupabaseUser().model_dump()


# Used in FetchUser to determine if user already exists
Existed = Optional[bool]
