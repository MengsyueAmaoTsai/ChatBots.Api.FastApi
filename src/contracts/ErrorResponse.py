from pydantic import BaseModel


class ErrorResponse(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: object
