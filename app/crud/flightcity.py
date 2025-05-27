from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import FlightCity


class CRUDFlightCity(CRUDBase):
    """Класс для CRUD модели FlightCity."""

    model = FlightCity

    async def get_cities_by_flight_id(
        self, session: AsyncSession, flight_id: int
    ) -> Sequence[FlightCity] | None:
        """Получение id городов по id полета."""
        db_cities = await session.execute(
            select(self.model)
            .where(self.model.flight_id == flight_id)
        )
        return db_cities.scalars().all()

    async def get_flights_by_city_id(
        self, session: AsyncSession, city_id: int
    ) -> Sequence[FlightCity] | None:
        """Получение id полетов по id города."""
        db_flights = await session.execute(
            select(self.model)
            .where(self.model.city_id == city_id)
        )
        return db_flights.scalars().all()

    async def get_flightcity_by_ids(
        self, session: AsyncSession, flight_id: int, city_id: int
    ) -> FlightCity | None:
        """Получение записи город - рейс по id."""
        db_flightcity = await session.execute(
            select(self.model)
            .where(
                self.model.flight_id == flight_id,
                self.model.city_id == city_id,
            )
        )
        return db_flightcity.scalars().first()


flightcity_crud = CRUDFlightCity()
