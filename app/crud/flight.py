from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Flight
from app.crud import CRUDBase
from app.schemas.flight import FlightDB


class CRUDFlight(CRUDBase):

    async def get_flights_by_date(
        self, session: AsyncSession, date: datetime
    ) -> Optional[FlightDB]:
        """Получение рейсов по дате."""

        db_flights = await session.execute(
            select(self.model).where(self.model.date_flight == date)
        )
        return db_flights.scalars().all()

    async def get_flights_by_number(
        self, session: AsyncSession, number: str
    ) -> list[Optional[FlightDB]]:
        """Получение рейсов по номеру рейса."""

        db_flights = await session.execute(
            select(self.model).where(
                self.model.number == number,
            )
        )
        return db_flights.scalars().all()

    async def get_flight_by_number_and_date(
        self, session: AsyncSession, number: str, date: datetime
    ) -> Optional[FlightDB]:
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
    ) -> Optional[FlightDB]:
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
