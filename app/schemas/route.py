from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.models.route import ROUTE_MAX_LENGHT


class RouteCreate(BaseModel):
    from_city: str = Field(..., min_length=3, max_length=ROUTE_MAX_LENGHT)
    to_city: str = Field(..., min_length=3, max_length=ROUTE_MAX_LENGHT)
    cost: PositiveInt
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RouteUpdate(BaseModel):
    from_city: Optional[str] = Field(
        None, min_length=3, max_length=ROUTE_MAX_LENGHT
    )
    to_city: Optional[str] = Field(
        None, min_length=3, max_length=ROUTE_MAX_LENGHT
    )
    cost: Optional[PositiveInt]
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RouteDB(RouteCreate):
    id: int
