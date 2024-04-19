FROM python:3.12-alpine AS build

WORKDIR /app

COPY pyproject.toml pdm.lock ./

RUN pip install pdm && pdm install

COPY . . 

FROM python:3.12-alpine AS production

WORKDIR /app

COPY --from=build /app .
RUN pip install pdm

EXPOSE 10002

CMD ["pdm", "start"]