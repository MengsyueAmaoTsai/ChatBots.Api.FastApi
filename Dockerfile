FROM python:3.12-alpine AS build

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
# ENV PYTHONPATH="/app/src:$PYTHONPATH"

WORKDIR /app

COPY requirements.lock ./

RUN pip install --no-cache-dir -r requirements.lock

COPY . .

FROM python:3.12-alpine AS production

WORKDIR /app

COPY --from=build /app .

RUN pip install --no-cache-dir -r requirements.lock

EXPOSE 10004

CMD ["python", "./src/main.py", "--port", "10004" "--host", "0.0.0.0", "--environment", "Production"]