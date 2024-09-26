from web import WebApplication

builder = WebApplication.create_builder()

app = builder.build()

if __name__ == "__main__":
    app.run()
