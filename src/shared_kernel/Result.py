from dataclasses import dataclass
from typing import Optional

from .Error import Error


@dataclass(frozen=True)
class ResultT[TValue]:
    _is_success: bool
    _error: Error
    _value: Optional[TValue]

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def error(self) -> Error:
        return self._error

    @property
    def value(self) -> TValue:
        if self._value is None:
            raise ValueError("Value is None")

        return self._value

    @staticmethod
    def failure(error: Error) -> "ResultT[TValue]":
        return ResultT[TValue](False, error, None)

    @staticmethod
    def success(value: TValue) -> "ResultT[TValue]":
        return ResultT[TValue](True, Error.null(), value)


@dataclass(frozen=True)
class Result:
    _is_success: bool
    _error: Error

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def error(self) -> Error:
        raise NotImplementedError

    @staticmethod
    def failure(error: Error) -> "Result":
        return Result(False, error)

    @staticmethod
    def success() -> "Result":
        return Result(True, Error.null())
