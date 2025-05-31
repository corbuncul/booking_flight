"""Модуль класса модели пользователей."""

from datetime import date, datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, Column, Date, String
from sqlalchemy.orm import validates

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Класс модели пользователей."""

    username = Column(String(20), nullable=True, unique=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    phone = Column(String(50), nullable=True)

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
