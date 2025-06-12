"""Модуль класса модели пользователей."""

from datetime import date, datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import (
    validates,
    Mapped,
    mapped_column,
)

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Класс модели пользователей."""

    username: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(50))
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    tg_username: Mapped[str] = mapped_column(String(50), unique=True)
    birthday: Mapped[date]
    phone: Mapped[str] = mapped_column(String(50), nullable=True)

    @validates('username')
    def validate_username(self, key: str, username: str) -> str:
        """Валидирует имя пользователя."""
        if self.is_superuser and not username:
            raise ValueError('Username cannot be empty for superuser')
        return username

    @validates('birthday')
    def validate_birthday(self, key: str, birthday: date) -> str | date:
        """Функция валидации даты рождения."""
        delta = datetime.now().year - birthday.year
        if delta < 15 or delta > 100:
            raise ValueError(
                'Возраст должен превышать 15 лет и быть меньше 100 лет.',
            )
        return birthday

    def __repr__(self) -> str:
        return f'{self.name=} {self.surname=} {self.tg_username=}'
