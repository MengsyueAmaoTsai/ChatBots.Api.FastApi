from fastapi import APIRouter

from contracts import ApiRoutes, LineMessagingRequest, LineMessagingResponse
from domain.abstractions import ILineBotService
from usecases import CreateUserCommand, GetUserCommand, HelpCommand, ICommand, ListUsersCommand

from .ApiTags import ApiTags


class LineMessagingEndpoint:
    CHANNEL_ACCESS_TOKEN = "MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET = "059dc70ee4cae01e3df05ac5813ed971"

    def __init__(self, line_bot_service: ILineBotService) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path=ApiRoutes.LINE_MESSAGING,
            endpoint=self.send_line_command,
            methods=["POST"],
            response_model=LineMessagingResponse,
            tags=[ApiTags.LineMessaging],
        )

        self._line_bot_service = line_bot_service

    async def send_line_command(self, request: LineMessagingRequest) -> LineMessagingResponse:
        for event in request.events:
            if not self._is_valid_command(event.message.text):
                continue

            command_text = event.message.text.strip().replace("/rc ", "")
            command = self.map_to_command(command_text)

            result = await self.handle_command(command)
            reply_message = f"Command {command.__class__.__name__} handled, result: {result}"

            reply_result = await self._line_bot_service.reply_text_message(
                reply_token=event.reply_token, text_message=reply_message
            )

            if reply_result.is_failure:
                print(f"Failed to reply message: {reply_result.error.message}")
            else:
                print(f"Replied message: {reply_message}")

        response = LineMessagingResponse(content="OK")
        return response

    def _is_valid_command(self, text: str) -> bool:
        return text.strip().startswith("/rc ")

    def map_to_command(self, text: str) -> ICommand:
        ## Get help
        if text == "-h" or text == "--help":
            return HelpCommand()

        ## Create new user
        if text.startswith("new user"):
            return CreateUserCommand()

        ## List users
        if text == "users list":
            return ListUsersCommand()

        ## Get user by id
        if text.startswith("user -id"):
            return GetUserCommand()

        raise Exception(f"Invalid command: {text}")

    async def handle_command(self, command: ICommand):
        """
        Handle command and returns Result or ResultT<TValue>
        """
        pass
