from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_routecost_exists,
    check_routecost_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import routecost_crud
from app.schemas.routecost import (
    RouteCostCreate,
    RouteCostResponse,
    RouteCostUpdate,
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[RouteCostResponse],
    dependencies=[Depends(current_superuser)],
)
async def get_all_routes(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех маршрутов. Только для суперюзеров."""
    return await routecost_crud.get_all(session)


@router.post(
    '/',
    response_model=RouteCostResponse,
    dependencies=[Depends(current_superuser)],
)
async def create_new_route(
    routecost: RouteCostCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание маршрута."""
    new_routecost = await routecost_crud.create(routecost, session)
    return new_routecost


@router.patch(
    '/{routecost_id}',
    response_model=RouteCostResponse,
    dependencies=[Depends(current_superuser)],
)
async def update_route(
    routecost_id: int,
    obj_in: RouteCostUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление маршрута."""
    routecost = await check_routecost_exists(session, routecost_id)
    if (obj_in.from_city_id is not None) and (obj_in.to_city_id is not None):
        await check_routecost_duplicate(
            session,
            from_city_id=obj_in.from_city_id,
            to_city_id=obj_in.to_city_id,
        )
    if obj_in.from_city_id is not None:
        await check_routecost_duplicate(
            session,
            from_city_id=obj_in.from_city_id,
            to_city_id=routecost.to_city_id,
        )
    if obj_in.to_city_id is not None:
        await check_routecost_duplicate(
            session,
            from_city_id=routecost.from_city_id,
            to_city_id=obj_in.to_city_id,
        )
    db_routecost = await routecost_crud.update(routecost, obj_in, session)
    return db_routecost


@router.delete(
    '/{routecost_id}',
    response_model=RouteCostResponse,
    dependencies=[Depends(current_superuser)],
)
async def delete_route(
    routecost_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление маршрута."""
    routecost = await check_routecost_exists(session, routecost_id)
    db_routecost = await routecost_crud.remove(routecost, session)
    return db_routecost
