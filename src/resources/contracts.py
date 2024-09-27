from datetime import datetime

from pydantic import BaseModel, Field


class SignalResponse(BaseModel):
    """"""

    id: str
    source_id: str = Field(alias="sourceId")
    origin: str
    symbol: str
    time: datetime
    trade_type: str = Field(alias="tradeType")
    quantity: float
    latency: int
    status: str
    created_time_utc: datetime = Field(alias="createdTimeUtc")
