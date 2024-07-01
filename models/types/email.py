# /models/types/email.py

from pydantic import BaseModel


class Email(BaseModel):
    email: str
