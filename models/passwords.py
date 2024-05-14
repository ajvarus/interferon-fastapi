# models/password.py

from pydantic import BaseModel
from typing import Dict

class Passwords(BaseModel):
    passwords: Dict[str, str]
