from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt
)

from app.core.constants import BOARD_MAX_LENGHT, FLIGHT_MAX_LENGHT
from .city import CityDB


class FlightCreate(BaseModel):
    number: str = Field(..., min_length=5, max_length=FLIGHT_MAX_LENGHT)
    board: Optional[str] = Field(
        ..., max_length=BOARD_MAX_LENGHT
    )
    routes: list[CityDB] #???
    date_flight: datetime
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class FlightUpdate(BaseModel):
    number: Optional[str] = Field(
        None, min_length=5, max_length=FLIGHT_MAX_LENGHT
    )
    board: Optional[str] = Field(
        None, min_length=3, max_length=BOARD_MAX_LENGHT
    )
    date_flight: Optional[datetime]
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class FlightDB(FlightCreate):
    id: int
