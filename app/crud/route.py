from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Route
from app.crud import CRUDBase
from app.schemas.route import RouteDB


class CRUDRoute(CRUDBase):

    async def get_routes_by_cities(
        self,
        session: AsyncSession,
        *,
        from_city: str | None = None,
        to_city: str | None = None
    ) -> list[Optional[RouteDB]]:
        """Получение маршрутов по городам."""
        query = select(self.model)
        if from_city is not None:
            query = query.where(self.model.from_city == from_city)
        if to_city is not None:
            query = query.where(self.model.to_city == to_city)
        db_routes = await session.execute(query)
        return db_routes.scalars().all()


route_crud = CRUDRoute(Route)
