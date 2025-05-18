from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RouteCost
from app.crud import CRUDBase
from app.schemas.routecost import RouteCostResponse


class CRUDRouteCost(CRUDBase):
    """Класс для CRUD модели RouteCost."""

    async def get_cost_by_cities(
        self, session: AsyncSession, from_city_id: int, to_city_id: int
    ) -> list[RouteCostResponse | None]:
        """Получение стоимости маршрута между городами."""
        db_routes = await session.execute(
            select(self.model).where(
                self.model.from_city_id == from_city_id,
                self.model.to_city_id == to_city_id,
            )
        )
        return db_routes.scalars().all()


routecost_crud = CRUDRouteCost(RouteCost)
