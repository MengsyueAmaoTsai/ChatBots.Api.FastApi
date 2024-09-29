from assertpy import assert_that

from shared_kernel import SingleValueObject


class TestSingleValueObject(SingleValueObject[str]):
    """ """


class SingleValueObjectTests:
    def test_to_string_when_value_is_not_none_should_return_value(self) -> None:
        value = "value"
        value_object = TestSingleValueObject(value)

        assert_that(str(value_object)).is_equal_to(value)
