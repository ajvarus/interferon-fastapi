

from pydantic import BaseModel
from typing import Optional



class SupabaseUser(BaseModel):
    user: Optional[dict] = None
    session: Optional[dict] = None