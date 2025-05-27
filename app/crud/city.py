from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import City


class CRUDCity(CRUDBase):
    """Класс для CRUD модели City."""

    model = City

    async def get_city_by_name(
        self, session: AsyncSession, name: str
    ) -> City | None:
        """Получение города по названию."""
        db_city = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return db_city.scalars().first()

    async def get_city_by_code(
        self, session: AsyncSession, code: str
    ) -> City | None:
        db_city = await session.execute(
            select(self.model).where(self.model.code == code)
        )
        return db_city.scalars().first()


city_crud = CRUDCity()
