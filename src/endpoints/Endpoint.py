from abc import ABC
from typing import Any

from contracts import ErrorResponse
from shared_kernel import Error, ErrorType

type ActionResultBase = Any
type ActionResult[T] = ActionResultBase | T


class Endpoint(ABC):
    """"""

    async def handle_failure[T](self, error: Error) -> ActionResult[T]:
        def get_error_info() -> tuple[str, int]:
            match error.type:
                case ErrorType.Validation:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.1", 400

                case ErrorType.Unauthorized:
                    return "https://datatracker.ietf.org/doc/html/rfc7235#section-3.1", 401

                case ErrorType.Forbidden:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.3", 403

                case ErrorType.NotFound:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.4", 404

                case ErrorType.Conflict:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8", 409

                case ErrorType.Unexpected:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.1", 500

                case ErrorType.Unavailable:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4", 503

                case _:
                    return "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.1", 500

        rfc_url, status = get_error_info()

        return ErrorResponse(
            type=rfc_url,
            statusCode=status,
            title=error.code,
            detail=error.message,
            instance=None,
        )
