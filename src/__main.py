from fastapi import FastAPI, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent

configuration = Configuration(
    access_token="MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser("059dc70ee4cae01e3df05ac5813ed971")


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/api/v1/line-messaging")
async def send_line_command(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
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


@app.post("/telegram-command")
async def send_telegram_command(request: Request):
    return {"statusCode": 200}


@app.post("/slack-command")
async def send_slack_command(request: Request):
    return {"statusCode": 200}


@app.post("/discord-command")
async def send_discord_command(request: Request):
    return {"statusCode": 200}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10002,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
