from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RouteCost
from app.crud import CRUDBase


class CRUDRouteCost(CRUDBase[RouteCost]):
    """Класс для CRUD модели RouteCost."""

    model = RouteCost

    async def get_cost_by_cities(
        self, session: AsyncSession, from_city_id: int, to_city_id: int
    ) -> RouteCost | None:
        """Получение стоимости маршрута между городами."""
        db_routes = await session.execute(
            select(self.model).where(
                self.model.from_city_id == from_city_id,
                self.model.to_city_id == to_city_id,
            )
        )
        return db_routes.scalars().first()


routecost_crud = CRUDRouteCost()
