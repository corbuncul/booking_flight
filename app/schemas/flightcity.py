from pydantic import BaseModel, ConfigDict, Field


class FlightCityCreate(BaseModel):
    city_id: int
    flight_id: int
    order: int = Field(..., ge=0, description="Порядок города в маршруте")
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class FlightCityUpdate(BaseModel):
    city_id: int | None = None
    flight_id: int | None = None
    order: int | None = Field(None, ge=0, description="Порядок города в маршруте")
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class FlightCityDB(FlightCityCreate):
    id: int
