from .LineMessagingRequest import LineMessagingRequest, MessagingEventRequest
from .LineMessagingResponse import LineMessagingResponse


class ApiRoutes:
    LINE_MESSAGING = "/api/v1/line-messaging"


__all__ = ["ApiRoutes", "LineMessagingResponse", "LineMessagingRequest", "MessagingEventRequest"]
