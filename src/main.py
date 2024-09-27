from hosting import WebApplication

builder = WebApplication.create_builder()

builder.services.add_endpoints()

app = builder.build()

app.use_request_debugging()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
