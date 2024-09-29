from abc import ABC, abstractmethod
from functools import reduce
from operator import xor
from typing import Any, Iterable


class ValueObject(ABC):
    def __eq__(self, value: object) -> bool:
        if value is None or not isinstance(value, self.__class__):
            return False

        return self._values_are_equal(value)

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return reduce(lambda x, y: xor(x, hash(y)), self.get_atomic_values(), 0)

    @abstractmethod
    def get_atomic_values(self) -> Iterable[Any]:
        """Return the atomic values that make up this value object."""
        pass

    def _values_are_equal(self, other: "ValueObject") -> bool:
        return list(self.get_atomic_values()) == list(other.get_atomic_values())
