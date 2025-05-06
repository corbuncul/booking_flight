from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.core.constants import TicketStatus
from app.schemas.passenger import PassengerDB
from app.schemas.city import CityDB
from app.schemas.flight import FlightDB


class TicketCreate(BaseModel):
    passenger_id: int
    flight_id: int
    from_city_id: int
    to_city_id: int
    number: str | None
    status: TicketStatus = Field(default=TicketStatus.BOOKED)
    created_at: datetime = Field(default_factory=datetime.now)
    paid_date: datetime | None
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketUpdate(BaseModel):
    number: str | None
    status: TicketStatus = Field(default=TicketStatus.BOOKED)
    paid_date: datetime | None = Field(default=datetime.now)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketDB(TicketCreate):
    id: int
    final_price: float
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketResponse(BaseModel):
    id: int
    passenger: PassengerDB
    flight: FlightDB
    from_city: CityDB
    to_city: CityDB
    status: str
    created_at: datetime
    final_price: float
    number: str | None
    paid_date: datetime | None
    model_config = ConfigDict(extra='forbid', from_attributes=True)
