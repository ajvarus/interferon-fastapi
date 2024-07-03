# /errors/types/session_error_codes.py

from enum import Enum

from ..error_info import ErrorInfo


class SessionErrorCode(Enum):
    SESSION_ALREADY_EXISTS = ErrorInfo(
        code=701,
        symbol="SESSION_ALREADY_EXISTS",
        message="User already has an active session.",
    )
