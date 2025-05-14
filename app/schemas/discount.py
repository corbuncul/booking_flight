from pydantic import BaseModel, ConfigDict


class DiscountCreate(BaseModel):
    code: str
    discount_percent: float
    is_active: bool
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class DiscountUpdate(BaseModel):
    code: str | None
    discount_percent: float | None
    is_active: bool | None
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class DiscountDB(DiscountCreate):
    id: int
