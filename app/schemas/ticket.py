from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import TicketStatus


class TicketCreate(BaseModel):
    passenger_id: int
    flight_id: int
    from_city_id: int
    to_city_id: int
    number: str | None = None
    discount_code: str | None = Field(None, exclude=True)
    final_price: float = Field(exclude=True)
    status: TicketStatus = Field(default=TicketStatus.BOOKED)
    created_at: datetime = Field(default_factory=datetime.now)
    paid_date: datetime | None = None
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketUpdate(BaseModel):
    number: str | None
    status: TicketStatus = Field(default=TicketStatus.BOOKED)
    paid_date: datetime = Field(default=datetime.now)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketDB(TicketCreate):
    id: int
    discount_code: str | None
    final_price: float
    model_config = ConfigDict(extra='forbid', from_attributes=True)
