# RichillCapital.ChatBots.Api

## Commands

### Install Dependencies

```bash
pdm install
```

### Build

```bash

```

### Run Development

```bash
pdm run dev
```

### Run Production

```bash
pdm start
```

Visit open api documentation: <https://127.0.0.1:8000/swagger> or <http://127.0.0.1:10000/swagger>

### Docker Build

```bash
docker build . -t chat-bots-api:latest
```

### Docker Run

```bash
docker run -d -it -p 10002:10002 --restart=always --name chat-bots-api chat-bots-api:latest
```
