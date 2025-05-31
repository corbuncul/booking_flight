from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.filters import UserFilter
from app.models import User


class CRUDUser(CRUDBase):
    """Класс запросов к БД, связанные с пользователями."""

    model = User

    async def get_users_by_filter(
        self,
        user_filter: UserFilter,
        session: AsyncSession,
    ) -> Sequence[User]:
        """Функция фильтрации пользователей из БД."""
        query = select(User)
        query = user_filter.filter(query)
        result = await session.execute(query)
        return result.scalars().all()


user_crud = CRUDUser()
