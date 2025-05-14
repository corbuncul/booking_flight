from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud import CRUDBase
from app.models import FlightCity
from app.schemas.flightcity import FlightCityResponse


class CRUDFlightCity(CRUDBase):

    async def get_cities_by_flight_id(
        self, session: AsyncSession, flight_id: int
    ) -> list[FlightCityResponse | None]:
        """Получение городов по id полета."""
        db_cities = await session.execute(
            select(self.model)
            .options(joinedload(self.model.city))
            .where(self.model.flight_id == flight_id)
        )
        return db_cities.scalars().all()

    async def get_flights_by_city_id(
        self, session: AsyncSession, city_id: int
    ) -> list[FlightCityResponse | None]:
        db_flights = await session.execute(
            select(self.model)
            .options(joinedload(self.model.flight))
            .where(self.model.city_id == city_id)
        )
        return db_flights.scalars().all()

    async def get_flightcity_by_ids(
        self, session: AsyncSession, flight_id: int, city_id: int
    ) -> FlightCityResponse | None:
        db_flightcity = await session.execute(
            select(self.model)
            .options(
                joinedload(self.model.flight), joinedload(self.model.city)
            )
            .where(
                self.model.flight_id == flight_id,
                self.model.city_id == city_id,
            )
        )
        return db_flightcity.scalars().first()


flightcity_crud = CRUDFlightCity(FlightCity)
