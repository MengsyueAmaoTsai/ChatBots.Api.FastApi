from domain import LineBotService
from domain.abstractions import ILineBotService
from hosting import WebApplication
from infrastructure.resources import ResourceService
from line.messaging import LineMessagingClient

builder = WebApplication.create_builder()

## Common services
builder.services.add_scoped(LineMessagingClient)

## Domain services
builder.services.add_scoped(ResourceService)

## Application services
builder.services.add_commands()
builder.services.add_scoped(ILineBotService, LineBotService)


## Presentation - Endpoints
builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
