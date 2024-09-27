from enum import Enum


class ErrorType(Enum):
    Null = 0
    Validation = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    Conflict = 409
    Unexpected = 500
    Unavailable = 503


class Error:
    def __init__(self, type: ErrorType, code: str, message: str) -> None:
        self.__type = type
        self.__code = code
        self.__message = message

    @property
    def type(self) -> ErrorType:
        return self.__type

    @property
    def code(self) -> str:
        return self.__code

    @property
    def message(self) -> str:
        return self.__message

    @staticmethod
    def null() -> "Error":
        return Error(ErrorType.Null, "NoError", str())

    @staticmethod
    def create(type: ErrorType, code: str, message: str) -> "Error":
        return Error(type, code, message)

    @staticmethod
    def invalid(code: str, message: str) -> "Error":
        return Error(ErrorType.Validation, code, message)

    @staticmethod
    def unauthorized(code: str, message: str) -> "Error":
        return Error(ErrorType.Unauthorized, code, message)

    @staticmethod
    def forbidden(code: str, message: str) -> "Error":
        return Error(ErrorType.Forbidden, code, message)

    @staticmethod
    def not_found(code: str, message: str) -> "Error":
        return Error(ErrorType.NotFound, code, message)

    @staticmethod
    def conflict(code: str, message: str) -> "Error":
        return Error(ErrorType.Conflict, code, message)

    @staticmethod
    def unexpected(code: str, message: str) -> "Error":
        return Error(ErrorType.Unexpected, code, message)

    @staticmethod
    def unavailable(code: str, message: str) -> "Error":
        return Error(ErrorType.Unavailable, code, message)
