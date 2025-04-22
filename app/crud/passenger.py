from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Passenger
from app.schemas.passenger import PassengerDB


class CRUDPassenger(CRUDBase):

    async def get_passengers_by_names(
        self,
        session: AsyncSession,
        *,
        surname: str | None = None,
        name: str | None = None,
    ) -> list[Optional[PassengerDB]]:
        """Получение пассажиров по фамилии и имени."""
        query = select(self.model)
        if surname is not None:
            query = query.where(self.model.surname == surname)
        if name is not None:
            query = query.where(self.model.name == name)
        db_passenger = await session.execute(query)
        return db_passenger.scalars().all()

    async def get_passengers_by_date_flight(
        self, session: AsyncSession, date_flight: datetime
    ) -> list[Optional[PassengerDB]]:
        db_passenger = await session.execute(
            select(self.model).where(
                self.model.tickets.flight.date_flight == date_flight
            )
        )
        return db_passenger.scalars().all()


passenger_crud = CRUDPassenger(Passenger)
