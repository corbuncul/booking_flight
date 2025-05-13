from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_city_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import city_crud
from app.schemas.city import CityCreate, CityDB, CityUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[CityDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_cities(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех населенных пунктов. Только для суперюзеров."""
    return await city_crud.get_all(session)


@router.post(
    '/',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_city(
    city: CityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание населенного пункта."""
    new_city = await city_crud.create(city, session)
    return new_city


@router.patch(
    '/{city_id}',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)],
)
async def update_city(
    city_id: int,
    obj_in: CityUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление населенного пункта."""
    city = await check_city_exists(session, city_id)
    db_city = await city_crud.update(city, obj_in, session)
    return db_city


@router.delete(
    '/{route_id}',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_city(
    city_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление населенного пункта."""
    city = await check_city_exists(session, city_id)
    db_city = await city_crud.remove(city, session)
    return db_city
