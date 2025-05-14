"""Импорты класса Base и всех моделей для Alembic."""

from app.core.db import Base  # noqa: F401
from app.models import (
    City,
    Discount,
    Flight,
    FlightCity,
    Passenger,
    RouteCost,
    Ticket,
    User,
)  # noqa: F401
