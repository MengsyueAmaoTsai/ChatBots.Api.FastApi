from pydantic import BaseModel


class LineMessagingResponse(BaseModel):
    messages: list[str]
