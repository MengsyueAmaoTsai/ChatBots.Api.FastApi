from pydantic import BaseModel


class LineMessagingResponse(BaseModel):
    content: str
