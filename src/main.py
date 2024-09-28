from domain import LineBotService
from domain.abstractions import ILineBotService
from hosting import WebApplication
from infrastructure.resources import ResourceService
from line.messaging import LineMessagingClient
from usecases import CommandSender
from usecases.abstractions import ICommandSender
from usecases.users import GetUserCommandHandler

builder = WebApplication.create_builder()

## Domain services
builder.services.add_scoped(ResourceService)

## Line bot service
builder.services.add_scoped(LineMessagingClient)
builder.services.add_scoped(ILineBotService, LineBotService)

## Application services
builder.services.add_scoped(ICommandSender, CommandSender)

handler_types = [GetUserCommandHandler]
for type in handler_types:
    builder.services.add_scoped(type)

## Presentation - Endpoints
builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
