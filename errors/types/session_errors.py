# /errors/types/session_errors.py

from ..error_codes import SessionErrorCode


class SessionError(Exception):
    def __init__(self, error: SessionErrorCode, description: str = "") -> None:
        self.error = error.value
        self.description = description
        super().__init__(f"{error.value.code}: {error.value.message}")

    def to_dict(self) -> dict[str, int | str]:
        return {
            "code": self.error.code,
            "symbol": self.error.symbol,
            "message": self.error.message,
            "description": self.description,
        }
