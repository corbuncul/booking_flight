from datetime import date, datetime

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
    PHONE_MAX_LENGHT,
)


class PassengerCreate(BaseModel):
    """Схема создания пользователя."""

    name: str = Field(..., max_length=NAME_MAX_LENGHT)
    surname: str = Field(..., max_length=NAME_MAX_LENGHT)
    phone: str | None = Field(None, max_length=PHONE_MAX_LENGHT)
    email: EmailStr | None = Field(None, max_length=NAME_MAX_LENGHT)
    birthday: date | None
    doc_number: str | None = Field(None, max_length=DOC_MAX_LENGHT)
    tg_id: str | None
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, values: date):
        """Проверка даты рождения."""
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        delta = datetime.now().year - values.year
        if delta < 0 or delta > 100:
            raise ValueError(
                "Возраст должен быть от 0 до 100 лет.",
            )
        return values


class PassengerUpdate(PassengerCreate):
    """Схема обговления пользователя."""

    name: str | None
    surname: str | None


class PassengerDB(PassengerCreate):
    """Схема пользователя для вывода из БД."""

    id: int

    @computed_field
    def full_name(self) -> str:
        """Вычисляемое поле полного имени."""
        return f"{self.name} {self.surname}"

    @computed_field
    def age(self) -> str:
        """Вычисляемое поле возраста."""
        today = date.today()
        delta = relativedelta(today, self.birthday)
        return f"{delta.years} лет, {delta.months} месяцев и {delta.days} дней"
