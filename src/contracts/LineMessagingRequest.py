from typing import Optional

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    id: str
    text: str
    type: str
    quote_token: Optional[str] = Field(alias="quoteToken")

    class Config:
        populate_by_name = True


class DeliveryContextRequest(BaseModel):
    is_redelivery: bool = Field(alias="isRedelivery")

    class Config:
        populate_by_name = True


class EventSourceRequest(BaseModel):
    type: str
    user_id: str = Field(alias="userId")

    class Config:
        populate_by_name = True


class MessagingEventRequest(BaseModel):
    type: str
    message: MessageRequest
    webhook_event_id: str = Field(alias="webhookEventId")
    delivery_context: DeliveryContextRequest = Field(alias="deliveryContext")
    timestamp: int
    source: EventSourceRequest
    reply_token: str = Field(alias="replyToken")
    mode: str

    class Config:
        populate_by_name = True


class LineMessagingRequest(BaseModel):
    """"""

    destination: str
    events: list[MessagingEventRequest]
