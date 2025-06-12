from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Discount


class CRUDDiscount(CRUDBase[Discount]):
    """Класс для CRUD модели Discount."""

    model = Discount

    async def get_discount_by_code(
        self, session: AsyncSession, code: str
    ) -> Discount | None:
        """Получение действующей скидки по коду."""
        db_discount = await session.execute(
            select(self.model).where(
                self.model.code == code,
                self.model.is_active.is_(True)
            )
        )
        return db_discount.scalars().first()


discount_crud = CRUDDiscount()
