from .LineMessagingRequest import LineMessagingRequest, MessagingEventRequest


class ApiRoutes:
    LINE_MESSAGING = "/api/v1/line-messaging"


__all__ = ["ApiRoutes", "LineMessagingRequest", "MessagingEventRequest"]
