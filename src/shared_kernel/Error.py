from dataclasses import dataclass
from enum import Enum


class ErrorType(Enum):
    Validation = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    Conflict = 409
    Unexpected = 500
    Unavailable = 503


@dataclass(frozen=True)
class Error:
    type: ErrorType
    code: str
    message: str

    @staticmethod
    def create(error_type: ErrorType, code: str, message: str) -> "Error":
        return Error(error_type, code, message)
