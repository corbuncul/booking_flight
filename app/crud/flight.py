from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Flight
from app.crud import CRUDBase
from app.schemas import FlightDB


class CRUDFlight(CRUDBase):
    """Класс для CRUD модели Flight."""

    async def get_flights_by_date(
        self, session: AsyncSession, date: datetime
    ) -> Sequence[FlightDB] | None:
        """Получение рейсов по дате."""

        db_flights = await session.execute(
            select(self.model).where(self.model.date_flight == date)
        )
        return db_flights.scalars().all()

    async def get_flights_by_number(
        self, session: AsyncSession, number: str
    ) -> Sequence[FlightDB] | None:
        """Получение рейсов по номеру рейса."""

        db_flights = await session.execute(
            select(self.model).where(
                self.model.number == number,
            )
        )
        return db_flights.scalars().all()

    async def get_flight_by_number_and_date(
        self, session: AsyncSession, number: str, date: datetime
    ) -> FlightDB | None:
        """Получение рейса по номеру и дате."""
        db_flight = await session.execute(
            select(self.model).where(
                self.model.number == number, self.model.date_flight == date
            )
        )
        return db_flight.scalars().first()

    async def get_flight_by_parameters(
        self,
        session: AsyncSession,
        *,
        number: str | None = None,
        date: datetime | None = None,
        board_number: str | None = None,
    ) -> Sequence[FlightDB] | None:
        """Получение рейса по различным параметрам."""
        query = select(self.model)
        if number is not None:
            query = query.where(self.model.number == number)
        if date is not None:
            query = query.where(self.model.date_flight == date)
        if board_number is not None:
            query.where(self.model.board_number == board_number)
        db_flight = await session.execute(query)
        return db_flight.scalars().all()


flight_crud = CRUDFlight(Flight)
