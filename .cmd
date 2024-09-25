#!/bin/bash

IMAGE_NAME=chat-bots-api:latest
SERVICE_PORT=10002
CONTAINER_PORT=10002
SERVICE_NAME=chat-bots-api

case $1 in 
    build)
        docker build -t $IMAGE_NAME .
        ;;
    start)
        docker run -d -it -p $SERVICE_PORT:$CONTAINER_PORT --restart=always --name $SERVICE_NAME $IMAGE_NAME
        ;;
    stop)
        docker stop $SERVICE_NAME && docker rm $SERVICE_NAME
        ;;
    restart)
        ./cmd build
        ./cmd stop
        ./cmd start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|build}"
        exit 1
        ;;
esac