# /graphic/types/password.py

import strawberry


@strawberry.input
class PasswordInput:
    password_name: str
    username: str
    password: str


@strawberry.type
class PasswordRequest:
    user_id: str
    password_name: str
    username: str
    encrypted_password: str


@strawberry.type
class PasswordResponse:
    id: strawberry.ID
    password_name: str
    username: str
    encrypted_password: str

    def to_dict(self) -> dict[str, int | str]:
        return {
            "id": self.id,
            "password_name": self.password_name,
            "encrypted_password": self.encrypted_password,
        }


@strawberry.type
class PasswordFetchResponse:
    id: strawberry.ID
    group_id: strawberry.ID
    password_name: str
    username: str
    decrypted_password: str


@strawberry.type
class PasswordCacheResponse:
    id: strawberry.ID
    decrypted_password: str


@strawberry.input
class PasswordUpdateInput:
    id: strawberry.ID
    password_name: str
    password: str


@strawberry.input
class PasswordDeleteInput:
    id: strawberry.ID
    password_name: str
