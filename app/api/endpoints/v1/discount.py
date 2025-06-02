from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_discount_exists,
    check_discount_code_dublicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import discount_crud
from app.schemas import DiscountCreate, DiscountDB, DiscountUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[DiscountDB],
)
async def get_all_discounts(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех скидок."""
    return await discount_crud.get_all(session)


@router.get(
    '/{discount_id}',
    response_model=DiscountDB,
)
async def get_by_id(
    discount_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение скидки по id."""
    return await discount_crud.get(discount_id, session)


@router.get(
    '/code/{discount_code}',
    response_model=DiscountDB,
)
async def get_discount_by_code(
    discount_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение скидки по коду."""
    return await discount_crud.get_discount_by_code(session, discount_code)


@router.post(
    '/',
    response_model=DiscountDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_discount(
    discount: DiscountCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание скидки. Только для суперюзеров."""
    await check_discount_code_dublicate(
        session=session, discount_code=discount.code
    )
    new_discount = await discount_crud.create(discount, session)
    discount_db, *_ = await discount_crud.save_changes(
        [new_discount,], session
    )
    return discount_db


@router.patch(
    '/{discount_id}',
    response_model=DiscountDB,
    dependencies=[Depends(current_superuser)],
)
async def update_discount(
    discount_id: int,
    obj_in: DiscountUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление скидки. Только для суперюзеров."""
    discount = await check_discount_exists(session, discount_id)
    db_discount = await discount_crud.update(discount, obj_in, session)
    return db_discount


@router.delete(
    '/{discount_id}',
    response_model=DiscountDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_discount(
    discount_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление скидки. Только для суперюзеров."""
    discount = await check_discount_exists(session, discount_id)
    db_discount = await discount_crud.remove(discount, session)
    return db_discount
