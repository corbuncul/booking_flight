from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_route_exists,
    check_route_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import route_crud
from app.schemas.route import (
    RouteCreate,
    RouteDB,
    RouteUpdate
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[RouteDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_routes(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех маршрутов. Только для суперюзеров."""
    return await route_crud.get_all(session)


@router.post(
    '/',
    response_model=RouteDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_route(
    route: RouteCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание маршрута."""
    new_route = await route_crud.create(route, session)
    return new_route


@router.patch(
    '/{route_id}',
    response_model=RouteDB,
    dependencies=[Depends(current_superuser)],
)
async def update_route(
    route_id: int,
    obj_in: RouteUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление маршрута."""
    route = await check_route_exists(session, route_id)
    if (obj_in.from_town is not None) and (obj_in.to_town is not None):
        await check_route_duplicate(
            session, from_town=obj_in.from_town, to_town=obj_in.to_town
        )
    if obj_in.from_town is not None:
        await check_route_duplicate(
            session, from_town=obj_in.from_town, to_town=route.to_town
        )
    if obj_in.to_town is not None:
        await check_route_duplicate(
            session, from_town=route.from_town, to_town=obj_in.to_town
        )
    db_route = await route_crud.update(route, obj_in, session)
    return db_route


@router.delete(
    '/{route_id}',
    response_model=RouteDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_route(
    route_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление маршрута."""
    route = await check_route_exists(session, route_id)
    db_route = await route_crud.remove(route, session)
    return db_route
