from datetime import date

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_future_date_flight,
    check_flight_duplicate,
    check_flight_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import flight_crud
from app.schemas import (
    FlightCreate,
    FlightDB,
    FlightUpdate,
)


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
    '/future',
    response_model=list[FlightDB],
)
async def get_future_flight(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех будущих рейсов."""
    return await flight_crud.get_future(session)


@router.get(
    '/get_by_parameters',
    response_model=list[FlightDB],
)
async def get_by_parameters(
    session: AsyncSession = Depends(get_async_session),
    flight_number: str | None = None,
    date_flight: date | None = None,
    board_number: str | None = None,
):
    """Список рейсов по параметрам."""
    return await flight_crud.get_flight_by_parameters(
        session, number=flight_number,
        date_flight=date_flight,
        board_number=board_number
    )


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
    check_future_date_flight(flight.date_flight)
    new_flight = await flight_crud.create(flight, session)
    db_flight, *_ = await flight_crud.save_changes([new_flight,], session)
    return db_flight


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
        check_future_date_flight(obj_in.date_flight)
        await check_flight_duplicate(
            session, flight.number, obj_in.date_flight
        )

    return await flight_crud.update(flight, obj_in, session)
