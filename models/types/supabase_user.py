

from pydantic import BaseModel
from typing import Optional



class SupabaseUser(BaseModel):
    user: Optional[dict] = {}
    session: Optional[dict] = {}