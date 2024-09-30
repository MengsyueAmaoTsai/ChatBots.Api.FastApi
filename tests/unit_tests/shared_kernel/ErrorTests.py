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

        validation_error = Error.invalid(ERROR_MESSAGE)
        validation_error2 = Error.invalid(ERROR_CODE, ERROR_MESSAGE)

        assert_that(validation_error.type).is_equal_to(ErrorType.Validation)
        assert_that(validation_error.code).is_equal_to(ErrorType.Validation.name)
        assert_that(validation_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(validation_error2.type).is_equal_to(ErrorType.Validation)
        assert_that(validation_error2.code).is_equal_to(ERROR_CODE)
        assert_that(validation_error2.message).is_equal_to(ERROR_MESSAGE)

        unauthorized_error = Error.unauthorized(ERROR_MESSAGE)
        unauthorized_error2 = Error.unauthorized(ERROR_CODE, ERROR_MESSAGE)

        assert_that(unauthorized_error.type).is_equal_to(ErrorType.Unauthorized)
        assert_that(unauthorized_error.code).is_equal_to(ErrorType.Unauthorized.name)
        assert_that(unauthorized_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(unauthorized_error2.type).is_equal_to(ErrorType.Unauthorized)
        assert_that(unauthorized_error2.code).is_equal_to(ERROR_CODE)
        assert_that(unauthorized_error2.message).is_equal_to(ERROR_MESSAGE)

        forbidden_error = Error.forbidden(ERROR_MESSAGE)
        forbidden_error2 = Error.forbidden(ERROR_CODE, ERROR_MESSAGE)

        assert_that(forbidden_error.type).is_equal_to(ErrorType.Forbidden)
        assert_that(forbidden_error.code).is_equal_to(ErrorType.Forbidden.name)
        assert_that(forbidden_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(forbidden_error2.type).is_equal_to(ErrorType.Forbidden)
        assert_that(forbidden_error2.code).is_equal_to(ERROR_CODE)
        assert_that(forbidden_error2.message).is_equal_to(ERROR_MESSAGE)

        not_found_error = Error.not_found(ERROR_MESSAGE)
        not_found_error2 = Error.not_found(ERROR_CODE, ERROR_MESSAGE)

        assert_that(not_found_error.type).is_equal_to(ErrorType.NotFound)
        assert_that(not_found_error.code).is_equal_to(ErrorType.NotFound.name)
        assert_that(not_found_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(not_found_error2.type).is_equal_to(ErrorType.NotFound)
        assert_that(not_found_error2.code).is_equal_to(ERROR_CODE)
        assert_that(not_found_error2.message).is_equal_to(ERROR_MESSAGE)

        conflict_error = Error.conflict(ERROR_MESSAGE)
        conflict_error2 = Error.conflict(ERROR_CODE, ERROR_MESSAGE)

        assert_that(conflict_error.type).is_equal_to(ErrorType.Conflict)
        assert_that(conflict_error.code).is_equal_to(ErrorType.Conflict.name)
        assert_that(conflict_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(conflict_error2.type).is_equal_to(ErrorType.Conflict)
        assert_that(conflict_error2.code).is_equal_to(ERROR_CODE)
        assert_that(conflict_error2.message).is_equal_to(ERROR_MESSAGE)

        unexpected_error = Error.unexpected(ERROR_MESSAGE)
        unexpected_error2 = Error.unexpected(ERROR_CODE, ERROR_MESSAGE)

        assert_that(unexpected_error.type).is_equal_to(ErrorType.Unexpected)
        assert_that(unexpected_error.code).is_equal_to(ErrorType.Unexpected.name)
        assert_that(unexpected_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(unexpected_error2.type).is_equal_to(ErrorType.Unexpected)
        assert_that(unexpected_error2.code).is_equal_to(ERROR_CODE)
        assert_that(unexpected_error2.message).is_equal_to(ERROR_MESSAGE)

        unavailable_error = Error.unavailable(ERROR_MESSAGE)
        unavailable_error2 = Error.unavailable(ERROR_CODE, ERROR_MESSAGE)

        assert_that(unavailable_error.type).is_equal_to(ErrorType.Unavailable)
        assert_that(unavailable_error.code).is_equal_to(ErrorType.Unavailable.name)
        assert_that(unavailable_error.message).is_equal_to(ERROR_MESSAGE)

        assert_that(unavailable_error2.type).is_equal_to(ErrorType.Unavailable)
        assert_that(unavailable_error2.code).is_equal_to(ERROR_CODE)
        assert_that(unavailable_error2.message).is_equal_to(ERROR_MESSAGE)

        null_error = Error.null()

        assert_that(null_error.type).is_equal_to(ErrorType.Null)
        assert_that(null_error.code).is_equal_to(ErrorType.Null.name)
        assert_that(null_error.message).is_equal_to(str())
