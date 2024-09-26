from fastapi import APIRouter, Request

from services import LineMessagingService


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
        self.line_messaging_service = LineMessagingService()

    async def send_line_command(self, request: Request):
        signature = request.headers["X-Line-Signature"]
        body = await request.body()
        body = body.decode()

        try:
            events = self.line_messaging_service.parse_request(body, signature)
            print("Parsed events: ", events)

        except InvalidSignatureError:
            print("Invalid signature")
            raise HTTPException(status_code=400, detail="Invalid signature")

        for event in events:
            if not isinstance(event, MessageEvent):
                continue

            if not isinstance(event.message, TextMessageContent):
                continue

            print("Received message: ", event.message.text)
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)],
                )
            )

        return {"statusCode": 200}
