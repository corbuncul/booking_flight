from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import (
    BOARD_MAX_LENGHT,
    FLIGHT_MAX_LENGHT,
    FLIGHT_MIN_LENGHT,
)


class FlightCreate(BaseModel):
    number: str = Field(
        ..., min_length=FLIGHT_MIN_LENGHT, max_length=FLIGHT_MAX_LENGHT
    )
    board: str | None = Field(..., max_length=BOARD_MAX_LENGHT)
    date_flight: datetime
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class FlightUpdate(BaseModel):
    number: str | None = Field(
        None, min_length=FLIGHT_MIN_LENGHT, max_length=FLIGHT_MAX_LENGHT
    )
    board: str | None = Field(None, max_length=BOARD_MAX_LENGHT)
    date_flight: datetime | None
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class FlightDB(FlightCreate):
    id: int
