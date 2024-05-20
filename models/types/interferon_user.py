

from pydantic import BaseModel
from datetime import datetime

class InterferonUser(BaseModel):
    user_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    last_active: datetime | str | None = None

    def is_default(self):
        return self.model_dump() == InterferonUser().model_dump()