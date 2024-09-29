from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    type: str
    title: str
    status_code: int = Field(alias="statusCode")
    detail: str
    instance: object
