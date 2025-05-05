from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.core.constants import (
    CODE_MAX_LENGHT,
    CODE_MIN_LENGHT
)


class CityCreate(BaseModel):
    name: str
    code: str = Field(
        ..., min_length=CODE_MIN_LENGHT, max_length=CODE_MAX_LENGHT
    )
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str] = Field(
        ..., min_length=CODE_MIN_LENGHT, max_length=CODE_MAX_LENGHT
    )
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityDB(CityCreate):
    id: int
