from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.city import CityDB
from app.schemas.flight import FlightDB


class FlightCityCreate(BaseModel):
    city_id: int
    flight_id: int
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class FlightCityUpdate(BaseModel):
    city_id: Optional[int]
    flight_id: Optional[int]
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class FlightCityDB(FlightCityCreate):
    id: int


class FlightCityResponse(BaseModel):
    id: int
    city: CityDB
    flight: FlightDB
    model_config = ConfigDict(from_attributes=True, extra='forbid')
