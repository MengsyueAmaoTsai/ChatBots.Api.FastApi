from shared_kernel import Error, Result


def test_result_success():
    result = Result.success()

    assert result.is_success
    assert not result.is_failure
    assert result.error == Error.null()


def test_result_failure():
    error = Error.invalid("error_code", "error_message")
    result = Result.failure(error)

    assert not result.is_success
    assert result.is_failure
    assert result.error == error
