from pydantic import (
    BaseModel,
    ConfigDict,
    PositiveInt
)


class TicketCreate(BaseModel):
    passenger: PositiveInt
    flight: PositiveInt
    number: str
    price: PositiveInt
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class TicketDB(TicketCreate):
    id: int
