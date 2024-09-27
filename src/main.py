from domain import LineBotService
from domain.abstractions import ILineBotService
from hosting import WebApplication
from infrastructure.resources import ResourceService
from line.messaging import LineMessagingClient

builder = WebApplication.create_builder()

## Domain services
builder.services.add_scoped(ResourceService)

## Line bot service
builder.services.add_scoped(LineMessagingClient)
builder.services.add_scoped(ILineBotService, LineBotService)

## Application services


## Presentation - Endpoints
builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
