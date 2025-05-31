"""Импорты класса Base и всех моделей для Alembic."""

from app.core.db import Base
from app.models import (
    City,
    Discount,
    Flight,
    FlightCity,
    Passenger,
    RouteCost,
    Ticket,
    User,
)

__all__ = (
    'Base',
    'City',
    'Discount',
    'Flight',
    'FlightCity',
    'Passenger',
    'RouteCost',
    'Ticket',
    'User'
)
