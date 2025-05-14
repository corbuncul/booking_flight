from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.discount import Discount


async def apply_discount(
    session: AsyncSession, discount_code: str, original_price: float
) -> float:
    discount = session.execute(
        select(Discount).where(
            Discount.code == discount_code, Discount.is_active is True
        )
    ).first()
    if not discount:
        return original_price  # Скидка не применяется
    return original_price * (1 - discount.discount_percent / 100)
