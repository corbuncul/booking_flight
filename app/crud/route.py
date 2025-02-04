from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Route
from app.crud import CRUDBase
from app.schemas.route import RouteDB


class CRUDRoute(CRUDBase):

    async def get_routes_by_towns(
        self,
        session: AsyncSession,
        *,
        from_town: str | None = None,
        to_town: str | None = None
    ) -> list[Optional[RouteDB]]:
        """Получение маршрутов по городам."""
        query = select(self.model)
        if from_town is not None:
            query = query.where(self.model.from_town == from_town)
        if to_town is not None:
            query = query.where(self.model.to_town == to_town)
        db_routes = await session.execute(query)
        return db_routes.scalars().all()


route_crud = CRUDRoute(Route)
