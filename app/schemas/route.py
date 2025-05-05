from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt


class RouteCreate(BaseModel):
    from_city_id: int
    to_city_id: int
    cost: PositiveInt
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RouteUpdate(BaseModel):
    from_city_id: Optional[int]
    to_city_id: Optional[int]
    cost: Optional[PositiveInt]
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RouteDB(RouteCreate):
    id: int
