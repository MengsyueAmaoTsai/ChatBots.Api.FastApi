from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/line-command")
async def send_line_command(request: Request):
    print(request)
    return {"statusCode": 200}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10002,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
