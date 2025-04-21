from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class CityCreate(BaseModel):
    name: str
    code: str = Field(..., min_length=3, max_length=5)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str] = Field(..., min_length=3, max_length=5)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityDB(CityCreate):
    id: int
