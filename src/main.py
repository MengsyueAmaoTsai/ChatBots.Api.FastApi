from domain import LineBotService
from domain.abstractions import ILineBotService
from hosting import WebApplication
from infrastructure.resources import ResourceService
from line.messaging import LineMessagingClient
from usecases.users import ListUsersCommandHandler

builder = WebApplication.create_builder()

## Domain services
builder.services.add_scoped(ResourceService)
builder.services.add_scoped(ILineBotService, LineBotService)


## Application services
command_handler_types = [ListUsersCommandHandler]

for handler_type in command_handler_types:
    builder.services.add_scoped(handler_type)

builder.services.add_scoped(LineMessagingClient)

## Presentation - Endpoints
builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
