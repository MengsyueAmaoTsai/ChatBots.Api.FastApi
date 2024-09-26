class MessageRequest:
    id: str
    text: str
    type: str
    quote_token: str


class DeliveryContextRequest:
    isRedelivery: bool


class EventSourceRequest:
    type: str
    userId: str


class MessagingEventRequest:
    type: str
    message: MessageRequest
    webhook_event_id: str
    delivery_context: DeliveryContextRequest
    timestamp: int
    source: EventSourceRequest
    reply_token: str
    mode: str


class SendReplyMessageRequest:
    """"""

    destination: str
    events: list[MessagingEventRequest]
