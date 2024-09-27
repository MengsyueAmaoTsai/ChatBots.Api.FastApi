import json
import time
from typing import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


class RequestDebuggingMiddleware(BaseHTTPMiddleware):
    ANONYMOUS_USER_NAME = "Anonymous"
    NO_HEADERS = "No headers"
    NO_QUERY_STRING = "No query string"
    NO_REQUEST_BODY = "No request body"
    NO_RESPONSE_BODY = "No response body"

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        method = request.method
        path = request.url.path
        remote_ip_address = request.client.host
        query_string = str(request.query_params)

        try:
            request_body_bytes = await request.body()
            request_body_info = (
                request_body_bytes.decode("utf-8") or self.NO_REQUEST_BODY
            )
        except Exception:
            request_body_info = ""

        start_time = time.time()
        print(
            f"Incoming request - {method} {path} from {self.ANONYMOUS_USER_NAME}@{remote_ip_address}"
        )

        response = await call_next(request)
        elapsed_time = time.time() - start_time
        status_code = response.status_code

        print(
            f"Outgoing response - {status_code} for {method} {path}. Elapsed: {elapsed_time:.2f}ms"
        )

        if status_code >= 400:
            return await self.handle_error_response(
                request=request,
                response=response,
                query_string=query_string,
                request_body_info=request_body_info,
            )

        return response

    async def handle_error_response(
        self,
        request: Request,
        response: Response,
        query_string: str,
        request_body_info: str,
    ) -> Response:
        request_headers = request.headers.items()
        response_headers = response.headers.items()

        request_headers_info = (
            "\n".join(f"{key}: {value}" for key, value in request_headers)
            if request_headers
            else self.NO_HEADERS
        )

        response_headers_info = (
            "\n".join(f"{key}: {value}" for key, value in response_headers)
            if response_headers
            else self.NO_HEADERS
        )

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body_string = response_body.decode("utf-8")

        self.log_details(
            request_headers_info=request_headers_info,
            query_string=query_string,
            request_body_info=json.dumps(request_body_info, indent=4),
            response_headers_info=response_headers_info,
            response_body_info=response_body_string,
        )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=response.headers,
        )

    def log_details(
        self,
        request_headers_info: str,
        query_string: str,
        request_body_info: str,
        response_headers_info: str,
        response_body_info: str,
    ):
        log_message = (
            "----- Request Details -----\n"
            f"Request Headers:\n{request_headers_info}\n"
            f"Query String: {query_string if query_string else self.NO_QUERY_STRING}\n"
            f"Request Body:\n{request_body_info if request_body_info else self.NO_REQUEST_BODY}\n"
            "----- Response Details -----\n"
            f"Response Headers:\n{response_headers_info}\n"
            f"Response Body:\n{response_body_info if response_body_info else self.NO_RESPONSE_BODY}\n"
        )

        print(log_message)
