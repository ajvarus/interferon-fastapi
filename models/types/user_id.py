# /models/types/user_id.py

from pydantic import BaseModel


class UserId(BaseModel):
    user_id: str
