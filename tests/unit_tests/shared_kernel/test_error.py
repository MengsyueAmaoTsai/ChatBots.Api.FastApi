from shared_kernel import Error, ErrorType


def test_error_create():
    error = Error.create(ErrorType.Validation, "code", "message")

    assert error.type is ErrorType.Validation
    assert error.code == "code"
    assert error.message == "message"


def test_error_invalid():
    error = Error.invalid("code", "message")

    assert error.type is ErrorType.Validation
    assert error.code == "code"
    assert error.message == "message"


def test_error_unauthorized():
    error = Error.unauthorized("code", "message")

    assert error.type is ErrorType.Unauthorized
    assert error.code == "code"
    assert error.message == "message"


def test_error_forbidden():
    error = Error.forbidden("code", "message")

    assert error.type is ErrorType.Forbidden
    assert error.code == "code"
    assert error.message == "message"


def test_error_not_found():
    error = Error.not_found("code", "message")

    assert error.type is ErrorType.NotFound
    assert error.code == "code"
    assert error.message == "message"


def test_error_conflict():
    error = Error.conflict("code", "message")

    assert error.type is ErrorType.Conflict
    assert error.code == "code"
    assert error.message == "message"


def test_error_unexpected():
    error = Error.unexpected("code", "message")

    assert error.type is ErrorType.Unexpected
    assert error.code == "code"
    assert error.message == "message"


def test_error_unavailable():
    error = Error.unavailable("code", "message")

    assert error.type is ErrorType.Unavailable
    assert error.code == "code"
    assert error.message == "message"
