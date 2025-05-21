from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Discount
from app.schemas import DiscountDB


class CRUDDiscount(CRUDBase):
    """Класс для CRUD модели Discount."""

    async def get_discount_by_code(
        self, session: AsyncSession, code: str
    ) -> DiscountDB | None:
        """Получение скидки по коду."""
        db_discount = await session.execute(
            select(self.model).where(self.model.code == code)
        )
        return db_discount.scalars().first()


discount_crud = CRUDDiscount(Discount)
