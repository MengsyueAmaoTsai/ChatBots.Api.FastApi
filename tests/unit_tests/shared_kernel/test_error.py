from shared_kernel import Error, ErrorType

error_code = "error_code"
error_message = "error_message"


def test_error_create():
    error = Error.create(ErrorType.Validation, error_code, error_message)

    assert error.type is ErrorType.Validation
    assert error.code == error_code
    assert error.message == error_message


def test_error_invalid():
    error = Error.invalid(error_code, error_message)

    assert error.type is ErrorType.Validation
    assert error.code == error_code
    assert error.message == error_message


def test_error_unauthorized():
    error = Error.unauthorized(error_code, error_message)

    assert error.type is ErrorType.Unauthorized
    assert error.code == error_code
    assert error.message == error_message


def test_error_forbidden():
    error = Error.forbidden(error_code, error_message)

    assert error.type is ErrorType.Forbidden
    assert error.code == error_code
    assert error.message == error_message


def test_error_not_found():
    error = Error.not_found(error_code, error_message)

    assert error.type is ErrorType.NotFound
    assert error.code == error_code
    assert error.message == error_message


def test_error_conflict():
    error = Error.conflict(error_code, error_message)

    assert error.type is ErrorType.Conflict
    assert error.code == error_code
    assert error.message == error_message


def test_error_unexpected():
    error = Error.unexpected(error_code, error_message)

    assert error.type is ErrorType.Unexpected
    assert error.code == error_code
    assert error.message == error_message


def test_error_unavailable():
    error = Error.unavailable(error_code, error_message)

    assert error.type is ErrorType.Unavailable
    assert error.code == error_code
    assert error.message == error_message
