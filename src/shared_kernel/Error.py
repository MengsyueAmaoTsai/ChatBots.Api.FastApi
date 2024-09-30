from dataclasses import dataclass
from enum import Enum
from typing import Any, overload


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
    type: ErrorType
    code: str
    message: str

    @staticmethod
    def null() -> "Error":
        return Error(ErrorType.Null, ErrorType.Null.name, "")

    @staticmethod
    def create(error_type: ErrorType, code: str, message: str) -> "Error":
        return Error(error_type, code, message)

    @overload
    @staticmethod
    def invalid(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def invalid(message: str) -> "Error": ...

    @staticmethod
    def invalid(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Validation, ErrorType.Validation.name, args[0])
        return Error(ErrorType.Validation, args[0], args[1])

    @overload
    @staticmethod
    def unauthorized(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def unauthorized(message: str) -> "Error": ...

    @staticmethod
    def unauthorized(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Unauthorized, ErrorType.Unauthorized.name, args[0])
        return Error(ErrorType.Unauthorized, args[0], args[1])

    @overload
    @staticmethod
    def forbidden(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def forbidden(message: str) -> "Error": ...

    @staticmethod
    def forbidden(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Forbidden, ErrorType.Forbidden.name, args[0])
        return Error(ErrorType.Forbidden, args[0], args[1])

    @overload
    @staticmethod
    def not_found(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def not_found(message: str) -> "Error": ...

    @staticmethod
    def not_found(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.NotFound, ErrorType.NotFound.name, args[0])
        return Error(ErrorType.NotFound, args[0], args[1])

    @overload
    @staticmethod
    def conflict(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def conflict(message: str) -> "Error": ...

    @staticmethod
    def conflict(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Conflict, ErrorType.Conflict.name, args[0])
        return Error(ErrorType.Conflict, args[0], args[1])

    @overload
    @staticmethod
    def unexpected(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def unexpected(message: str) -> "Error": ...

    @staticmethod
    def unexpected(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Unexpected, ErrorType.Unexpected.name, args[0])
        return Error(ErrorType.Unexpected, args[0], args[1])

    @overload
    @staticmethod
    def unavailable(code: str, message: str) -> "Error": ...

    @overload
    @staticmethod
    def unavailable(message: str) -> "Error": ...

    @staticmethod
    def unavailable(*args: Any, **kwargs: Any) -> "Error":
        if len(args) == 1:
            return Error(ErrorType.Unavailable, ErrorType.Unavailable.name, args[0])
        return Error(ErrorType.Unavailable, args[0], args[1])
