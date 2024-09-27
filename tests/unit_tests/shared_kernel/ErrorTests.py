from shared_kernel import Error, ErrorType

ERROR_CODE = "error_code"
ERROR_MESSAGE = "error_message"


class TestError:
    def test_create_should_create_error(self) -> None:
        error = Error.create(ErrorType.Validation, ERROR_CODE, "error_message")

        assert error.type == ErrorType.Validation
        assert error.code == ERROR_CODE
        assert error.message == "error_message"
