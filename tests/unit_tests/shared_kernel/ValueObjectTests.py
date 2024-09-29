from typing import Any, Iterable

from assertpy import assert_that

from shared_kernel import ValueObject


class TestValueObject(ValueObject):
    def __init__(self, string: str, number: int) -> None:
        self.string = string
        self.number = number

    def get_atomic_values(self) -> Iterable[Any]:
        yield self.string
        yield self.number


class ValueObjectTests:
    def test_equals_when_value_objects_have_the_same_values_should_return_true(self) -> None:
        object1 = TestValueObject("string", 1)
        object2 = TestValueObject("string", 1)

        assert_that(object1 == object2).is_true()

    def test_equals_when_value_objects_have_different_values_should_return_false(self) -> None:
        object1 = TestValueObject("string", 1)
        object2 = TestValueObject("different", 2)

        assert_that(object1 == object2).is_false()

    def test_get_hash_code_when_value_objects_have_the_same_values_should_return_the_same_hash_code(self) -> None:
        object1 = TestValueObject("string", 1)
        object2 = TestValueObject("string", 1)

        assert_that(hash(object1)).is_equal_to(hash(object2))

    def test_get_hash_code_when_value_objects_have_different_values_should_return_different_hash_codes(self) -> None:
        object1 = TestValueObject("string", 1)
        object2 = TestValueObject("different", 2)

        assert_that(hash(object1)).is_not_equal_to(hash(object2))
