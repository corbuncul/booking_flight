from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import discount_crud


async def apply_discount(
    session: AsyncSession, discount_code: str, original_price: float
) -> float:

    discount = await discount_crud.get_discount_by_code(session, discount_code)
    if not discount:
        return original_price  # Скидка не применяется
    return float(original_price * (1 - discount.discount_percent / 100))
