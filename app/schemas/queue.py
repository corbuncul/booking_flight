from datetime import date

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt
)


class QueueCreate(BaseModel):
    passenger: PositiveInt
    flight: PositiveInt
    create_date: date = Field(default_factory=date.today)
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class QueueDB(QueueCreate):
    id: int
