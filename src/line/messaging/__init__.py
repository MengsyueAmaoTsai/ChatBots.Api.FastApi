import httpx

from shared_kernel import Error, Result


class LineMessagingClient:
    """"""

    BASE_ADDRESS = "https://api.line.me"
    ACCESS_TOKEN = "MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="

    def __init__(self) -> None: ...

    async def send_reply_message(self, reply_token: str, message: str) -> Result:
        """"""
        async with httpx.AsyncClient(
            verify=False,
            event_hooks={"request": [self.set_bearer_token, self.log_request], "response": [self.log_response]},
        ) as client:
            response = await client.post(
                f"{self.BASE_ADDRESS}/v2/bot/message/reply",
                json={
                    "replyToken": reply_token,
                    "messages": [{"type": "text", "text": message}],
                },
            )

            return await self.handle_response(response)

    async def handle_response(self, response: httpx.Response) -> Result:
        if response.status_code >= 400:
            return Result.failure(Error.invalid("Validation", response.text))

        return Result.success()

    async def set_bearer_token(self, request: httpx.Request) -> None:
        request.headers["Authorization"] = f"Bearer {self.ACCESS_TOKEN}"

    async def log_request(self, request: httpx.Request) -> None:
        print("Out going request", request)

    async def log_response(self, response: httpx.Response) -> None:
        print("In coming response", response)
