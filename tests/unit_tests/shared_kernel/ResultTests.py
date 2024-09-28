from shared_kernel import Error, Result, ResultT

ERROR = Error.invalid(message="error_message")


class TestResult:
    """"""

    def test_success_should_create_success_result(self) -> None:
        result = Result.success()

        assert result.is_success
        assert not result.is_failure

    def test_failure_should_create_failure_result(self) -> None:
        result = Result.failure(ERROR)

        assert not result.is_success
        assert result.is_failure

    def test_equal_results_should_be_equal(self) -> None:
        result1 = Result.success()
        result2 = Result.success()

        assert result1 == result2

    def test_different_results_should_not_be_equal(self) -> None:
        result1 = Result.success()
        result2 = Result.failure(ERROR)

        assert result1 != result2


class TestResultT:
    """"""

    def test_success_should_create_success_result(self) -> None:
        expected_value = "value"
        result = ResultT[str].success(expected_value)

        assert result.is_success
        assert not result.is_failure
        assert result.value == expected_value
        assert result.error == Error.null()

    def test_failure_should_create_failure_result(self) -> None:
        result = ResultT[str].failure(ERROR)

        assert not result.is_success
        assert result.is_failure
        assert result.error == ERROR

        try:
            result.value
            assert False
        except ValueError:
            assert True

    def test_equal_results_should_be_equal(self) -> None:
        result1 = ResultT[str].success("value")
        result2 = ResultT[str].success("value")

        assert result1 == result2

    def test_different_results_should_not_be_equal(self) -> None:
        result1 = ResultT[str].success("value")
        result2 = ResultT[str].failure(ERROR)

        assert result1 != result2
