from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ErrorType(Enum):
    Null = 0
    Validation = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    Conflict = 409
    Unexpected = 500
    Unavailable = 503


@dataclass(frozen=True)
class Error:
    _NO_ERROR = "NoError"

    type: ErrorType
    code: str
    message: str

    @staticmethod
    def null() -> "Error":
        return Error(ErrorType.Null, Error._NO_ERROR, str())

    @staticmethod
    def create(type: ErrorType, code: str, message: str) -> "Error":
        return Error(type, code, message)

    @staticmethod
    def invalid(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Validation
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def unauthorized(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Unauthorized
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def forbidden(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Forbidden
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def not_found(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.NotFound
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def conflict(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Conflict
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def unexpected(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Unexpected
        return Error(error_type, code or error_type.name, message or str())

    @staticmethod
    def unavailable(code: Optional[str] = None, message: Optional[str] = None) -> "Error":
        error_type = ErrorType.Unavailable
        return Error(error_type, code or error_type.name, message or str())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Error):
            return False

        return self.type == other.type and self.code == other.code
