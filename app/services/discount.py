from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import discount_crud
from app.models.discount import Discount


async def apply_discount(
    session: AsyncSession,
    discount_code: str,
    original_price: float,
) -> float:
    """
    Применяет скидку к исходной цене.

    Args:
        session: Асинхронная сессия БД
        discount_code: Код скидки
        original_price: Исходная цена

    Returns:
        float: Окончательная цена со скидкой
    """
    discount: Discount | None = await discount_crud.get_discount_by_code(
        session, discount_code
    )
    if not discount:
        return original_price  # Скидка не применяется

    return float(original_price * (1 - discount.discount_percent / 100))
