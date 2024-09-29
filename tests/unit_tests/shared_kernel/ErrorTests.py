from assertpy import assert_that

from shared_kernel import Error, ErrorType

ERROR_CODE = "error_code"
ERROR_MESSAGE = "error_message"


class ErrorTests:
    def test_equals_when_with_same_types_and_same_messages_should_return_true(self) -> None:
        error = Error(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)

        assert_that(error.type).is_equal_to(ErrorType.Validation)
        assert_that(error.code).is_equal_to(ERROR_CODE)
        assert_that(error.message).is_equal_to(ERROR_MESSAGE)

    def test_equals_when_with_same_types_and_different_messages_should_return_false(self) -> None:
        error = Error(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)

        assert_that(error.type).is_equal_to(ErrorType.Validation)
        assert_that(error.code).is_equal_to(ERROR_CODE)
        assert_that(error.message).is_not_equal_to("another_message")

    def test_equals_when_with_different_types_and_same_messages_should_return_false(self) -> None:
        error = Error(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)

        assert_that(error.type).is_not_equal_to(ErrorType.Unauthorized)
        assert_that(error.code).is_equal_to(ERROR_CODE)
        assert_that(error.message).is_equal_to(ERROR_MESSAGE)

    def test_equals_when_with_different_types_and_different_messages_should_return_false(self) -> None:
        error = Error(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)

        assert_that(error.type).is_not_equal_to(ErrorType.Unauthorized)
        assert_that(error.code).is_not_equal_to("another_code")
        assert_that(error.message).is_not_equal_to("another_message")

    def test_create_should_create_error(self) -> None:
        error = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)

        assert_that(error.type).is_equal_to(ErrorType.Validation)
        assert_that(error.code).is_equal_to(ERROR_CODE)
        assert_that(error.message).is_equal_to(ERROR_MESSAGE)
