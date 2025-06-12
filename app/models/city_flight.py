from datetime import date, time

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from app.core.constants import (
    CODE_MAX_LENGHT,
    BOARD_MAX_LENGHT,
    FLIGHT_MAX_LENGHT,
    FlightStatus,
    NAME_MAX_LENGHT,
)
from app.core.db import Base


class City(Base):
    code: Mapped[str] = mapped_column(
        String(CODE_MAX_LENGHT), unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGHT))
    flights: Mapped[list['Flight']] = relationship(
        'Flight',
        secondary='flight_city',
        back_populates='cities',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.name}'


class Flight(Base):
    number: Mapped[str] = mapped_column(String(FLIGHT_MAX_LENGHT))
    board: Mapped[str | None] = mapped_column(
        String(BOARD_MAX_LENGHT), nullable=True
    )
    date_flight: Mapped[date]
    time_flight: Mapped[time]
    status: Mapped[FlightStatus]
    cities: Mapped[list['City']] = relationship(
        'City',
        secondary='flight_city',
        back_populates='flights',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.number} {self.date_flight}'


class FlightCity(Base):
    flight_id: Mapped[int] = mapped_column(ForeignKey('flight.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    order: Mapped[int]
