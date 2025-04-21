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
    name: str = Field(
        ..., min_length=1, max_length=NAME_MAX_LENGHT
    )
    surname: str = Field(
        ..., min_length=1, max_length=NAME_MAX_LENGHT
    )
    phone: Optional[str] = Field(
        None, min_length=1, max_length=PHONE_MAX_LENGHT
    )
    email: Optional[EmailStr] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )
    birthday: Optional[date]
    doc_nunber: Optional[str] = Field(
        None, min_length=1, max_length=DOC_MAX_LENGHT
    )
    tg_id: Optional[str]
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        delta = datetime.now().year - values.year
        if delta < 0 or delta > 100:
            raise ValueError(
                "Возраст должен быть от 0 до 100 лет.",
            )
        return values


class PassengerUpdate(PassengerCreate):
    name: Optional[str] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )
    surname: Optional[str] = Field(
        None, min_length=1, max_length=NAME_MAX_LENGHT
    )


class PassengerDB(PassengerCreate):
    id: int

    @computed_field
    def full_name(self) -> str:
        return f"{self.name} {self.surname}"

    @computed_field
    def age(self) -> str:
        today = date.today()
        delta = relativedelta(today, self.birthday)
        return f"{delta.years} лет, {delta.months} месяцев и {delta.days} дней"
