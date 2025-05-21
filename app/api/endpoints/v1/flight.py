from datetime import datetime

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_flight_duplicate,
    check_flight_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import city_crud, flight_crud, flightcity_crud
from app.schemas import (
    CityFlights,
    FlightCreate,
    FlightDB,
    FlightUpdate,
)
from app.schemas.flightcity import FlightCityResponse


router = APIRouter()


@router.get(
    '/',
    response_model=list[FlightDB],
)
async def get_all_flight(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех рейсов."""
    return await flight_crud.get_all(session)


@router.get(
    '/get_by_parameters',
    response_model=list[FlightDB],
)
async def get_by_parameters(
    session: AsyncSession = Depends(get_async_session),
    flight_number: str | None = None,
    date: datetime | None = None,
    board_number: str | None = None,
):
    """Список рейсов по параметрам."""
    return await flight_crud.get_flight_by_parameters(
        session, number=flight_number, date=date, board_number=board_number
    )


@router.get(
    '/by_city_id/{city_id}',
    response_model=list[FlightCityResponse],
)
async def get_by_city_id(
    city_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Список рейсов из города по id города."""
    return await flightcity_crud.get_flights_by_city_id(session, city_id)


@router.get(
    '/by_city_code/{city_code}',
    response_model=CityFlights,
)
async def get_by_city_code(
    city_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Список рейсов из города по коду города."""
    return await city_crud.get_city_by_code(session, city_code)


@router.get(
    '/by_city_name/{city_name}',
    response_model=CityFlights,
)
async def get_by_city_name(
    city_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Список рейсов из города по имени города."""
    return await city_crud.get_city_by_name(session, city_name)


@router.post(
    '/',
    response_model=FlightDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_flight(
    flight: FlightCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание рейса. Только для суперюзеров."""
    await check_flight_duplicate(session, flight.number, flight.date_flight)
    return await flight_crud.create(flight, session)


@router.delete(
    '/{flight_id}',
    response_model=FlightDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_flight(
    flight_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление рейса. Только для суперюзеров."""
    flight = await check_flight_exists(session, flight_id)
    return await flight_crud.remove(flight, session)


@router.patch(
    '/{flight_id}',
    response_model=FlightDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_flight(
    flight_id: int,
    obj_in: FlightUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Изменение рейса. Только для суперюзеров."""
    flight = await check_flight_exists(session, flight_id)

    if (obj_in.number is not None) and (obj_in.date_flight is not None):
        await check_flight_duplicate(
            session, obj_in.number, obj_in.date_flight
        )

    if obj_in.number is not None:
        await check_flight_duplicate(
            session, obj_in.number, flight.date_flight
        )

    if obj_in.date_flight is not None:
        await check_flight_duplicate(
            session, flight.number, obj_in.date_flight
        )

    return await flight_crud.update(flight, obj_in, session)
