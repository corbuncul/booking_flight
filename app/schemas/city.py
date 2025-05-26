from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import (
    CODE_MAX_LENGHT,
    CODE_MIN_LENGHT,
    NAME_MAX_LENGHT,
)


class CityCreate(BaseModel):
    name: str = Field(..., max_length=NAME_MAX_LENGHT)
    code: str = Field(
        ..., min_length=CODE_MIN_LENGHT, max_length=CODE_MAX_LENGHT
    )
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityUpdate(BaseModel):
    name: str | None = Field(None, max_length=NAME_MAX_LENGHT)
    code: str | None = Field(
        None, min_length=CODE_MIN_LENGHT, max_length=CODE_MAX_LENGHT
    )
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class CityDB(CityCreate):
    id: int
