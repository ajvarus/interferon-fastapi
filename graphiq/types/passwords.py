# /graphic/types/password.py

import strawberry

from typing import List, Optional


@strawberry.input
class PasswordInput:
    password_name: str
    password: str


@strawberry.type
class PasswordRequest:
    user_id: str
    password_name: str
    encrypted_password: str


@strawberry.type
class PasswordResponse:
    id: strawberry.ID
    password_name: str
    encrypted_password: str


@strawberry.type
class PasswordFetchResponse:
    id: strawberry.ID
    password_name: str
    decrypted_password: str
