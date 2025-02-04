from datetime import date, datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    EmailStr,
    Field,
    field_validator,
)

from app.models.passenger import (
    DOC_MAX_LENGHT,
    NAME_MAX_LENGHT,
    PHONE_MAX_LENGHT
)


class PassengerCreate(BaseModel):
    first_name: str = Field(
        ..., min_length=1, max_length=NAME_MAX_LENGHT
    )
    surname: str = Field(
        ..., min_length=1, max_length=NAME_MAX_LENGHT
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )
    phone: Optional[str] = Field(
        None, min_length=1, max_length=PHONE_MAX_LENGHT
    )
    email: Optional[EmailStr] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )
    date_of_birth: Optional[date]
    doc_nunber: Optional[str] = Field(
        None, min_length=1, max_length=DOC_MAX_LENGHT
    )
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values


class PassengerUpdate(PassengerCreate):
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )
    surname: Optional[str] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )


class PassengerDB(PassengerCreate):
    id: int

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.surname}"

    @computed_field
    def age(self) -> str:
        today = date.today()
        delta = relativedelta(today, self.date_of_birth)
        return f"{delta.years} лет, {delta.months} месяцев и {delta.days} дней"
