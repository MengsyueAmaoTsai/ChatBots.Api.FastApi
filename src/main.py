from web import WebApplication

builder = WebApplication.create_builder()

app = builder.build()

app.map_endpoints()

if __name__ == "__main__":
    app.run()
