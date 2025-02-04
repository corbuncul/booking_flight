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
        first_name: str | None = None,
    ) -> list[Optional[PassengerDB]]:
        """Получение пассажиров по фамилии и имени."""
        query = select(self.model)
        if surname is not None:
            query = query.where(self.model.surname == surname)
        if first_name is not None:
            query = query.where(self.model.first_name == first_name)
        db_passenger = await session.execute(query)
        return db_passenger.scalars().all()


passenger_crud = CRUDPassenger(Passenger)
