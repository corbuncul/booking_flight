from pydantic import BaseModel, ConfigDict

from . import CityDB


class RouteCostCreate(BaseModel):
    from_city_id: int
    to_city_id: int
    cost: float
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RouteCostUpdate(BaseModel):
    from_city_id: int | None
    to_city_id: int | None
    cost: float | None
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RoutCostDB(RouteCostCreate):
    id: int


class RouteCostResponse(BaseModel):
    id: int
    from_city: CityDB
    to_city: CityDB
    cost: float
    model_config = ConfigDict(from_attributes=True, extra='forbid')
