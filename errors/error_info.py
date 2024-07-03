# /errors/error_info.py

from typing import NamedTuple


class ErrorInfo(NamedTuple):
    code: int
    symbol: str
    message: str
