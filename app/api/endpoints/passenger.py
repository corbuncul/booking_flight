from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_passenger_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import passenger_crud
from app.schemas.passenger import (
    PassengerCreate,
    PassengerDB,
    PassengerUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def get_all_passengers(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех пассажиров. Только для суперюзеров."""
    return await passenger_crud.get_all(session)


@router.post(
    '/',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_passener(
    passenger: PassengerCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание пассажира."""
    new_passenger = await passenger_crud.create(passenger, session)
    return new_passenger


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
    """Обновление пассажира."""
    passenger = await check_passenger_exists(session, passenger_id)
    db_passenger = await passenger_crud.update(passenger, obj_in, session)
    return db_passenger


@router.delete(
    '/{route_id}',
    response_model=PassengerDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_passenger(
    passenger_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление пассажира."""
    passenger = await check_passenger_exists(session, passenger_id)
    db_passenger = await passenger_crud.remove(passenger, session)
    return db_passenger
