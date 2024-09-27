from dataclasses import dataclass
from typing import Optional

from .Error import Error


@dataclass(frozen=True)
class Result:
    _is_success: bool
    _error: Optional[Error]

    @classmethod
    def success(cls) -> "Result":
        return cls(True, None)

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
    def error(self) -> Optional[Error]:
        return self._error
