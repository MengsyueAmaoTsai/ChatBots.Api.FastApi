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
    def __init__(self, type: ErrorType, code: str, message: str):
        self.type = type
        self.code = code
        self.message = message

    @staticmethod
    def create(type: ErrorType, code: str, message: str) -> "Error":
        return Error(type, code, message)
