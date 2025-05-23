from datetime import datetime

from pydantic import BaseModel, ConfigDict

from . import CityDB, PassengerDB, FlightDB, TicketDB


class PassengerTickets(PassengerDB):
    tickets: list[TicketDB]


class TicketResponse(BaseModel):
    id: int
    passenger: PassengerDB
    flight: FlightDB
    from_city: CityDB
    to_city: CityDB
    status: str
    created_at: datetime
    discount_code: str | None
    final_price: float
    number: str | None
    paid_date: datetime | None
    model_config = ConfigDict(extra='forbid', from_attributes=True)
