from assertpy import assert_that

from shared_kernel import Error
from shared_kernel.monad import Result, ResultT

ERROR = Error.invalid("error_message")


class ResultTTests:
    def test_failure_when_given_error_should_create_failure_result_with_error(self) -> None:
        result = ResultT[int].failure(ERROR)

        assert_that(result.is_success).is_false()
        assert_that(result.is_failure).is_true()
        assert_that(result.error).is_equal_to(ERROR)

    def test_success_when_given_value_should_create_success_result_with_value(self) -> None:
        expected = 1
        result = ResultT[int].success(expected)

        assert_that(result.is_success).is_true()
        assert_that(result.is_failure).is_false()
        assert_that(result.error).is_equal_to(Error.null())
        assert_that(result.value).is_equal_to(expected)

    def test_equals_when_success_results_with_different_values_should_return_false(self) -> None:
        result1 = ResultT[int].success(1)
        result2 = ResultT[int].success(2)

        assert_that(result1).is_not_equal_to(result2)

    def test_equals_when_success_results_with_same_values_should_return_true(self) -> None:
        result1 = ResultT[int].success(1)
        result2 = ResultT[int].success(1)

        assert_that(result1).is_equal_to(result2)


class ResultTests:
    def test_failure_when_given_error_should_create_failure_result_with_error(self) -> None:
        result = Result.failure(ERROR)

        assert_that(result.is_success).is_false()
        assert_that(result.is_failure).is_true()
        assert_that(result.error).is_equal_to(ERROR)

    def test_success_should_create_success_result_with_null_error(self) -> None:
        result = Result.success()

        assert_that(result.is_success).is_true()
        assert_that(result.is_failure).is_false()
        assert_that(result.error).is_equal_to(Error.null())

    def test_equals_when_success_results_should_return_true(self) -> None:
        result1 = Result.success()
        result2 = Result.success()

        assert_that(result1).is_equal_to(result2)

    def test_equals_when_failure_results_with_same_errors_should_return_true(self) -> None:
        result1 = Result.failure(ERROR)
        result2 = Result.failure(ERROR)

        assert_that(result1).is_equal_to(result2)
