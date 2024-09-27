from enum import Enum


class ErrorType(Enum):
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
    def create(type: ErrorType, code: str, message: str) -> "Error":
        return Error(type, code, message)
