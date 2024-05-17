from pydantic import BaseModel


class SignUpCredentials(BaseModel):
    email: str
    password: str

class SignInCredentials(BaseModel):
    email: str
    password: str