from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_city_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import city_crud, flightcity_crud
from app.schemas import (
    CityCreate,
    CityDB,
    CityFlights,
    CityUpdate,
    FlightCityResponse
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CityDB],
)
async def get_all_cities(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех населенных пунктов."""
    return await city_crud.get_all(session)


@router.get(
    '/{city_id}',
    response_model=CityDB,
)
async def get_by_id(
    city_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение населенного пункта по id."""
    return await city_crud.get(city_id, session)


@router.get(
    '/code/{city_code}',
    response_model=CityFlights,
)
async def get_by_code(
    city_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение населенного пункта по коду."""
    return await city_crud.get_city_by_code(session, city_code)


@router.get(
    '/name/{city_name}',
    response_model=CityFlights,
)
async def get_by_name(
    city_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение населенного пункта по имени."""
    return await city_crud.get_city_by_name(session, city_name)


@router.get(
        '/by_flight_id/{flight_id}',
        response_model=list[FlightCityResponse],
)
async def get_by_flight_id(
    flight_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await flightcity_crud.get_cities_by_flight_id(session, flight_id)


@router.post(
    '/',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_city(
    city: CityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание населенного пункта. Только для суперюзеров."""
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
    """Обновление населенного пункта. Только для суперюзеров."""
    city = await check_city_exists(session, city_id)
    db_city = await city_crud.update(city, obj_in, session)
    return db_city


@router.delete(
    '/{city_id}',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_city(
    city_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление населенного пункта. Только для суперюзеров."""
    city = await check_city_exists(session, city_id)
    db_city = await city_crud.remove(city, session)
    return db_city
