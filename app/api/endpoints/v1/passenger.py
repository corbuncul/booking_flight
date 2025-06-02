from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_passenger_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import passenger_crud
from app.schemas import PassengerCreate, PassengerDB, PassengerUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[PassengerDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_passengers(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех пассажиров. Только для суперюзеров."""
    return await passenger_crud.get_all(session)


@router.get(
    '/by_date_flight/{date}',
    response_model=list[PassengerDB],
    dependencies=[Depends(current_superuser)],
)
async def get_passengers_by_date(
    date: datetime,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение пассажиров по дате вылета. Только для суперюзеров."""
    return await passenger_crud.get_passengers_by_date_flight(session, date)


@router.get(
    '/name',
    response_model=list[PassengerDB],
    dependencies=[Depends(current_superuser)],
)
async def get_passengers_by_name(
    session: AsyncSession = Depends(get_async_session),
    name: str | None = None,
    surname: str | None = None,
):
    """Получение пассажиров по имени или фамилии. Только для суперюзеров."""
    return passenger_crud.get_passengers_by_names(
        session, name=name, surname=surname
    )


@router.post(
    '/',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_passener(
    passenger: PassengerCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание пассажира. Только для суперюзеров."""
    new_passenger = await passenger_crud.create(passenger, session)
    db_passenger, *_ = await passenger_crud.save_changes(
        [new_passenger,], session
    )
    return db_passenger


@router.patch(
    '/{passenger_id}',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def update_passenger(
    passenger_id: int,
    obj_in: PassengerUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление пассажира. Только для суперюзеров."""
    passenger = await check_passenger_exists(session, passenger_id)
    db_passenger = await passenger_crud.update(passenger, obj_in, session)
    return db_passenger


@router.delete(
    '/{passenger_id}',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_passenger(
    passenger_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление пассажира. Только для суперюзеров."""
    passenger = await check_passenger_exists(session, passenger_id)
    db_passenger = await passenger_crud.remove(passenger, session)
    return db_passenger
