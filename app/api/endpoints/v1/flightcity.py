from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_city_exists,
    check_flight_exists,
    check_flightcity_exists,
    check_flightcity_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import flightcity_crud
from app.schemas import (
    FlightCityCreate,
    FlightCityResponse,
    FlightCityUpdate,
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[FlightCityResponse],
    dependencies=[Depends(current_superuser)],
)
async def get_all_flightcity(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех городов во всех рейсах. Только для суперюзеров."""
    return await flightcity_crud.get_all(session)


@router.post(
    '/',
    response_model=FlightCityResponse,
    dependencies=[Depends(current_superuser)],
)
async def create_new_flightcity(
    flightcity: FlightCityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление города в рейс. Только для суперюзеров."""
    await check_flight_exists(
        session=session,
        flight_id=flightcity.flight_id,
    )
    await check_city_exists(
        session=session,
        city_id=flightcity.city_id,
    )
    new_flightcity = await flightcity_crud.create(flightcity, session)
    return new_flightcity


@router.patch(
    '/{flightcity_id}',
    response_model=FlightCityResponse,
    dependencies=[Depends(current_superuser)],
)
async def update_flightcity(
    flightcity_id: int,
    obj_in: FlightCityUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление связи маршрут - город. Только для суперюзеров."""
    flightcity = await check_flightcity_exists(session, flightcity_id)
    if (obj_in.city_id is not None) and (obj_in.flight_id is not None):
        await check_flightcity_duplicate(
            session, flight_id=obj_in.flight_id, city_id=obj_in.city_id
        )
    if obj_in.flight_id is not None:
        await check_flightcity_duplicate(
            session, flight_id=obj_in.flight_id, city_id=flightcity.city_id
        )
    if obj_in.city_id is not None:
        await check_flightcity_duplicate(
            session, flight_id=flightcity.flight_id, city_id=obj_in.city_id
        )
    db_flightcity = await flightcity_crud.update(flightcity, obj_in, session)
    return db_flightcity


@router.delete(
    '/{flightcity_id}',
    response_model=FlightCityResponse,
    dependencies=[Depends(current_superuser)],
)
async def delete_flightcity(
    flightcity_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление связи город - рейс. Только для суперюзеров."""
    flightcity = await check_flightcity_exists(session, flightcity_id)
    db_flightcity = await flightcity_crud.remove(flightcity, session)
    return db_flightcity
