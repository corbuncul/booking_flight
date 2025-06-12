from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Flight, FlightCity


class CRUDFlight(CRUDBase[Flight]):
    """Класс для CRUD модели Flight."""

    model = Flight

    async def get_future(
        self, session: AsyncSession
    ) -> Sequence[Flight] | None:
        """Получение будущих рейсов."""

        db_flights = await session.execute(
            select(self.model).where(self.model.date_flight >= date.today())
        )
        return db_flights.scalars().all()

    async def get_flights_by_date(
        self, session: AsyncSession, date_flight: date
    ) -> Sequence[Flight] | None:
        """Получение рейсов по дате."""

        db_flights = await session.execute(
            select(self.model).where(self.model.date_flight == date_flight)
        )
        return db_flights.scalars().all()

    async def get_flights_by_number(
        self, session: AsyncSession, number: str
    ) -> Sequence[Flight] | None:
        """Получение рейсов по номеру рейса."""

        db_flights = await session.execute(
            select(self.model).where(
                self.model.number == number,
                self.model.date_flight >= date.today()
            )
        )
        return db_flights.scalars().all()

    async def get_flight_by_number_and_date(
        self, session: AsyncSession, number: str, date_flight: date
    ) -> Flight | None:
        """Получение рейса по номеру и дате."""
        db_flight = await session.execute(
            select(self.model).where(
                self.model.number == number,
                self.model.date_flight == date_flight
            )
        )
        return db_flight.scalars().first()

    async def get_flight_by_parameters(
        self,
        session: AsyncSession,
        *,
        number: str | None = None,
        date_flight: date | None = None,
        board_number: str | None = None,
    ) -> Sequence[Flight] | None:
        """Получение рейса по различным параметрам."""
        query = select(self.model)
        if number is not None:
            query = query.where(self.model.number == number)
        if date is not None:
            query = query.where(self.model.date_flight == date_flight)
        if board_number is not None:
            query.where(self.model.board == board_number)
        db_flight = await session.execute(query)
        return db_flight.scalars().all()

    async def get_flight_by_date_cities(
        self,
        session: AsyncSession,
        date_flight: date,
        from_city_id: int,
        to_city_id: int,
    ) -> Flight | None:
        """Получение рейса по дате и городам."""
        query = (
            select(self.model)
            .join(FlightCity)
            .where(
                self.model.date_flight == date_flight,
                FlightCity.city_id.in_([from_city_id, to_city_id]),
            )
        )
        result = await session.execute(query)
        return result.scalars().first()


flight_crud = CRUDFlight()
