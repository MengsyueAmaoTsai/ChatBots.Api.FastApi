from domain import ILineBotService, LineBotService
from hosting import WebApplication
from line.messaging import LineMessagingClient

builder = WebApplication.create_builder()

## Domain services
builder.services.add_scoped(ILineBotService, LineBotService)

builder.services.add_scoped(LineMessagingClient)

## Presentation - Endpoints
builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
