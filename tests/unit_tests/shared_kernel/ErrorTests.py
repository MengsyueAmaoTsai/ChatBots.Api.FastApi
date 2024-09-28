from shared_kernel import Error, ErrorType

ERROR_CODE = "error_code"
ERROR_MESSAGE = "error_message"


class TestError:
    def test_factory_methods_should_create_error(self) -> None:
        error = Error.create(ErrorType.Validation, ERROR_CODE, "error_message")

        assert error.type == ErrorType.Validation
        assert error.code == ERROR_CODE
        assert error.message == "error_message"

        validation_error = Error.invalid(ERROR_CODE, ERROR_MESSAGE)
        assert validation_error.type == ErrorType.Validation
        assert validation_error.code == ERROR_CODE
        assert validation_error.message == ERROR_MESSAGE

        validation_error2 = Error.invalid(message=ERROR_MESSAGE)
        assert validation_error2.type == ErrorType.Validation
        assert validation_error2.code == ErrorType.Validation.name
        assert validation_error2.message == ERROR_MESSAGE

        unauthorized_error = Error.unauthorized(ERROR_CODE, ERROR_MESSAGE)
        assert unauthorized_error.type == ErrorType.Unauthorized
        assert unauthorized_error.code == ERROR_CODE
        assert unauthorized_error.message == ERROR_MESSAGE

        unauthorized_error2 = Error.unauthorized(message=ERROR_MESSAGE)
        assert unauthorized_error2.type == ErrorType.Unauthorized
        assert unauthorized_error2.code == ErrorType.Unauthorized.name
        assert unauthorized_error2.message == ERROR_MESSAGE

        access_denied_error = Error.access_denied(ERROR_CODE, ERROR_MESSAGE)
        assert access_denied_error.type == ErrorType.AccessDenied
        assert access_denied_error.code == ERROR_CODE
        assert access_denied_error.message == ERROR_MESSAGE

        access_denied_error2 = Error.access_denied(message=ERROR_MESSAGE)
        assert access_denied_error2.type == ErrorType.AccessDenied
        assert access_denied_error2.code == ErrorType.AccessDenied.name
        assert access_denied_error2.message == ERROR_MESSAGE

        not_found_error = Error.not_found(ERROR_CODE, ERROR_MESSAGE)
        assert not_found_error.type == ErrorType.NotFound
        assert not_found_error.code == ERROR_CODE
        assert not_found_error.message == ERROR_MESSAGE

        not_found_error2 = Error.not_found(message=ERROR_MESSAGE)
        assert not_found_error2.type == ErrorType.NotFound
        assert not_found_error2.code == ErrorType.NotFound.name
        assert not_found_error2.message == ERROR_MESSAGE

        conflict_error = Error.conflict(ERROR_CODE, ERROR_MESSAGE)
        assert conflict_error.type == ErrorType.Conflict
        assert conflict_error.code == ERROR_CODE
        assert conflict_error.message == ERROR_MESSAGE

        conflict_error2 = Error.conflict(message=ERROR_MESSAGE)
        assert conflict_error2.type == ErrorType.Conflict
        assert conflict_error2.code == ErrorType.Conflict.name
        assert conflict_error2.message == ERROR_MESSAGE

        unexpected_error = Error.unexpected(ERROR_CODE, ERROR_MESSAGE)
        assert unexpected_error.type == ErrorType.Unexpected
        assert unexpected_error.code == ERROR_CODE
        assert unexpected_error.message == ERROR_MESSAGE

        unexpected_error2 = Error.unexpected(message=ERROR_MESSAGE)
        assert unexpected_error2.type == ErrorType.Unexpected
        assert unexpected_error2.code == ErrorType.Unexpected.name
        assert unexpected_error2.message == ERROR_MESSAGE

        unavailable_error = Error.unavailable(ERROR_CODE, ERROR_MESSAGE)
        assert unavailable_error.type == ErrorType.Unavailable
        assert unavailable_error.code == ERROR_CODE
        assert unavailable_error.message == ERROR_MESSAGE

        unavailable_error2 = Error.unavailable(message=ERROR_MESSAGE)
        assert unavailable_error2.type == ErrorType.Unavailable
        assert unavailable_error2.code == ErrorType.Unavailable.name
        assert unavailable_error2.message == ERROR_MESSAGE

    def test_equal_should_equals(self) -> None:
        error1 = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)
        error2 = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)
        assert error1 == error2

        error5 = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)
        error6 = Error.create(ErrorType.Validation, ERROR_CODE, "another_message")
        assert error5 == error6

    def test_equal_should_not_equals(self) -> None:
        error1 = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)
        error2 = Error.create(ErrorType.Unauthorized, ERROR_CODE, ERROR_MESSAGE)
        assert error1 != error2

        error3 = Error.create(ErrorType.Validation, ERROR_CODE, ERROR_MESSAGE)
        error4 = Error.create(ErrorType.Validation, "another_code", ERROR_MESSAGE)
        assert error3 != error4
