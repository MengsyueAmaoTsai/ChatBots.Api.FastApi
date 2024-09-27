from dataclasses import dataclass

from .Error import Error


@dataclass(frozen=True)
class Result:
    _is_success: bool
    _error: Error

    @classmethod
    def success(cls) -> "Result":
        return cls(True, Error.null())

    @classmethod
    def failure(cls, error: Error) -> "Result":
        return cls(False, error)

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def error(self) -> Error:
        if self.is_success:
            return Error.null()

        return self._error
