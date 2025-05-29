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
        """Получение городов по id полета, отсортированных по порядку."""
        db_cities = await session.execute(
            select(self.model)
            .where(self.model.flight_id == flight_id)
            .order_by(self.model.order)
        )
        return db_cities.scalars().all()

    async def get_flights_by_city_id(
        self, session: AsyncSession, city_id: int
    ) -> Sequence[FlightCity] | None:
        """Получение полетов по id города."""
        db_flights = await session.execute(
            select(self.model)
            .where(self.model.city_id == city_id)
            .order_by(self.model.order)
        )
        return db_flights.scalars().all()

    async def get_flightcity_by_ids(
        self, session: AsyncSession, flight_id: int, city_id: int
    ) -> FlightCity | None:
        """Получение записи город - рейс по id."""
        db_flightcity = await session.execute(
            select(self.model).where(
                self.model.flight_id == flight_id,
                self.model.city_id == city_id,
            )
        )
        return db_flightcity.scalars().first()

    async def get_max_order(
        self, session: AsyncSession, flight_id: int
    ) -> int:
        """Получение максимального порядкового номера для рейса."""
        result = await session.execute(
            select(self.model.order)
            .where(self.model.flight_id == flight_id)
            .order_by(self.model.order.desc())
        )
        max_order = result.scalar()
        return max_order if max_order is not None else -1


flightcity_crud = CRUDFlightCity()
