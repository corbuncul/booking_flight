from pydantic import BaseModel, ConfigDict

from . import CityDB, FlightDB


class FlightCityCreate(BaseModel):
    city_id: int
    flight_id: int
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class FlightCityUpdate(BaseModel):
    city_id: int | None
    flight_id: int | None
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class FlightCityDB(FlightCityCreate):
    id: int


class FlightCityResponse(BaseModel):
    id: int
    city: CityDB
    flight: FlightDB
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class CityFlights(CityDB):
    flights: list[FlightDB]


class FlightCities(FlightDB):
    routes: list[CityDB]
