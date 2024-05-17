

from pydantic import BaseModel
from datetime import datetime

class InterferonUser(BaseModel):
    user_id: str | None = None
    token: str | None = None
    supabase_token: str | None = None
    is_active: bool | None = None
    last_active: datetime | str | None = None