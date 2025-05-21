from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud import CRUDBase
from app.models import City
from app.schemas import CityFlights


class CRUDCity(CRUDBase):
    """Класс для CRUD модели City."""

    async def get_city_by_name(
        self, session: AsyncSession, name: str
    ) -> CityFlights | None:
        """Получение города по названию."""
        db_city = await session.execute(
            select(self.model)
            .options(joinedload(self.model.flights))
            .where(self.model.name == name)
        )
        return db_city.scalars().first()

    async def get_city_by_code(
        self, session: AsyncSession, code: str
    ) -> CityFlights | None:
        db_city = await session.execute(
            select(self.model)
            .options(joinedload(self.model.flights))
            .where(self.model.code == code)
        )
        return db_city.scalars().first()


city_crud = CRUDCity(City)
