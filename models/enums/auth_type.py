from enum import Enum


class AuthType(Enum):
    RESOLVE = "resolve"
    SIGNUP = "signup"
    SIGNIN = "signin"
    SIGNOUT = "signout"
