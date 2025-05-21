from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud import CRUDBase
from app.models import Passenger
from app.schemas import PassengerDB


class CRUDPassenger(CRUDBase):
    """Класс для CRUD модели Passenger."""

    async def get_passengers_by_names(
        self,
        session: AsyncSession,
        *,
        surname: str | None = None,
        name: str | None = None,
    ) -> Sequence[PassengerDB] | None:
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
    ) -> Sequence[PassengerDB] | None:
        """Получение пассажиров по дате вылета."""
        db_passenger = await session.execute(
            select(self.model)
            .options(
                joinedload(self.model.tickets),
                joinedload(self.model.tickets.flight),
            )
            .where(self.model.tickets.flight.date_flight == date_flight)
        )
        return db_passenger.scalars().all()


passenger_crud = CRUDPassenger(Passenger)
