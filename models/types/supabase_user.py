

from pydantic import BaseModel
from typing import Optional



class SupabaseUser(BaseModel):
    user: Optional[dict] = {}
    session: Optional[dict] = {}

    def is_default(self):
        return self.model_dump() == SupabaseUser().model_dump()