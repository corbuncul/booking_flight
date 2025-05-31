"""Модуль классов схем пользователей."""

from datetime import date
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Класс для схемы чтения пользователя."""

    name: str
    surname: Optional[str] = None
    tg_id: int
    tg_username: str
    birthday: date
    phone: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    """Класс для схемы создания пользователя."""

    username: Optional[str] = None
    name: str
    surname: Optional[str] = None
    tg_id: int
    tg_username: str
    birthday: date
    phone: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    """Класс для схемы обновления пользователя."""

    name: Optional[str] = None
    surname: Optional[str] = None
    tg_id: Optional[int] = None
    tg_username: Optional[str] = None
    is_subscribed: Optional[bool]
