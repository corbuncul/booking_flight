from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt
)

from app.models.ticket import PaidStatus


class TicketCreate(BaseModel):
    passenger_id: PositiveInt
    flight_id: PositiveInt
    number: Optional[str]
    created_at: datetime
    paid_date: Optional[datetime]
    status: PaidStatus = Field(default=PaidStatus.BOOKED)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketDB(TicketCreate):
    id: int
