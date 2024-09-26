from fastapi import APIRouter, HTTPException, Request


class LineMessagingEndpoint:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path="/api/v1/line-messaging",
            endpoint=self.send_line_command,
            methods=["POST"],
            response_model=None,
        )

        ## services

    async def send_line_command(self, request: Request) -> None:
        raise HTTPException(status_code=400, detail="Invalid signature")
        return {"statusCode": 200}
