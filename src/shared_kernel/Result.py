from .Error import Error


class ResultT[TValue]:
    is_success: bool
    error: Error
    value: TValue

    @staticmethod
    def failure(error: Error) -> "ResultT[TValue]":
        raise NotImplementedError()

    @staticmethod
    def success(value: TValue) -> "ResultT[TValue]":
        raise NotImplementedError()


class Result:
    is_success: bool
    error: Error

    @staticmethod
    def failure(error: Error) -> "Result":
        raise NotImplementedError()

    @staticmethod
    def success() -> "Result":
        raise NotImplementedError()
