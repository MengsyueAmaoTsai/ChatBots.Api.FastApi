from fastapi import APIRouter, HTTPException

from contracts import ApiRoutes, LineMessagingRequest, LineMessagingResponse
from domain.abstractions import ILineBotService
from endpoints.Endpoint import ActionResult
from shared_kernel import Error
from shared_kernel.Result import ResultT

from .ApiTags import ApiTags


class LineMessagingEndpoint:
    CHANNEL_ACCESS_TOKEN = "MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET = "059dc70ee4cae01e3df05ac5813ed971"

    def __init__(self, line_bot_service: ILineBotService) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path=ApiRoutes.LINE_MESSAGING,
            endpoint=self.handle,
            methods=["POST"],
            response_model=LineMessagingResponse,
            tags=[ApiTags.LineMessaging],
        )

        self._line_bot_service = line_bot_service

    async def handle(self, request: LineMessagingRequest) -> ActionResult[LineMessagingResponse]:
        messages: list[str] = []
        for event in request.events:
            if not self._is_valid_command(event.message.text):
                continue

            command_text = event.message.text.strip().replace("/rc ", "")
            handle_result = await self.send_command(command_text)

            if handle_result.is_failure:
                raise HTTPException(status_code=400, detail=handle_result.error.message)

            reply_message = handle_result.value

            reply_result = await self._line_bot_service.reply_text_message(
                reply_token=event.reply_token, text_message=reply_message
            )

            if reply_result.is_failure:
                print(f"Failed to reply message: {reply_result.error.message}")

            messages.append(reply_message)

        return LineMessagingResponse(messages=messages)

    def _is_valid_command(self, text: str) -> bool:
        return text.strip().startswith("/rc ")

    async def send_command(self, text_command: str) -> ResultT[str]:
        """
        TODO COMMANDS
        new -h: Show help message
        signals -h: Show help message
        signals list: Show signals list
        signals --id <id>: Show signal details
        """

        if text_command == "-v" or text_command == "--version":
            return ResultT[str].success("Richill Capital Chat Bots Api Version: 1.0.0")

        if text_command == "-h" or text_command == "--help":
            return ResultT[str].success("Help")

        return ResultT[str].failure(Error.invalid(message=f"Invalid command: {text_command}"))
