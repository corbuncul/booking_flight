from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import City
from app.schemas.city import CityDB


class CRUDCity(CRUDBase):
    """Класс для CRUD модели City."""

    async def get_city_by_name(
        self, session: AsyncSession, name: str
    ) -> CityDB | None:
        """Получение города по названию."""
        db_city = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return db_city.scalars().first()

    async def get_city_by_code(
        self, session: AsyncSession, code: str
    ) -> CityDB | None:
        db_city = await session.execute(
            select(self.model).where(self.model.code == code)
        )
        return db_city.scalars().first()


city_crud = CRUDCity(City)
