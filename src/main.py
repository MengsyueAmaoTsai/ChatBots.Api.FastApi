from builder import WebApplication
from endpoints import LineMessagingEndpoint
from usecases import CommandSender, ICommandSender

builder = WebApplication.create_builder()

## Add Domain Services

## Add Application Services
builder.services.add_scoped(ICommandSender, CommandSender)

## Add Infrastructure Services

## Add Presentation Services
endpoint_types = [LineMessagingEndpoint]

for endpoint in endpoint_types:
    builder.services.add_scoped(endpoint, endpoint)

app = builder.build()

if __name__ == "__main__":
    app.run()
