from abc import ABC
from typing import Any, Iterable

from .ValueObject import ValueObject


class SingleValueObject[TValue](ValueObject, ABC):
    def __init__(self, value: TValue) -> None:
        self._value = value

    @property
    def value(self) -> TValue:
        return self._value

    def get_atomic_values(self) -> Iterable[Any]:
        yield self.value

    def __str__(self) -> str:
        return str(self.value)
