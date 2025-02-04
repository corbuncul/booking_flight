from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.flight import flight_crud
from app.crud.passenger import passenger_crud
from app.crud.queue import queue_crud
from app.crud.route import route_crud
from app.crud.ticket import ticket_crud
from app.models import Flight, Passenger, Queue, Route, Ticket


async def check_flight_duplicate(
    session: AsyncSession,
    flight_number: str,
    flight_date: datetime,
) -> None:
    """Провверка на дублирование рейса"""
    flight_id = await flight_crud.get_flight_by_number_and_date(
        session, flight_number, flight_date
    )
    if flight_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Рейс с таким номером на эту дату уже существует!',
        )


async def check_flight_exists(
    session: AsyncSession,
    flight_id: int,
) -> Flight:
    """Проверка существования рейса"""
    flight = await flight_crud.get(flight_id, session)
    if flight is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Рейс не найден!'
        )
    return flight


async def check_passenger_exists(
    session: AsyncSession,
    passenger_id: int,
) -> Passenger:
    """Проверка существования пассажира"""
    passenger = await passenger_crud.get(passenger_id, session)
    if passenger is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Пассажир не найден!'
        )
    return passenger


async def check_queue_exists(
    session: AsyncSession,
    queue_id: int,
) -> Queue:
    """Проверка существования записи пассажира на рейс."""
    queue = await queue_crud.get(queue_id, session)
    if queue is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Запись не найдена!'
        )
    return queue


async def check_ticket_exists(
    session: AsyncSession,
    ticket_id: int,
) -> Ticket:
    """Проверка существования билета"""
    ticket = await ticket_crud.get(ticket_id, session)
    if ticket is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='билет не найден!'
        )
    return ticket


async def check_route_exists(
    session: AsyncSession,
    route_id: int,
) -> Route:
    """Проверка существования маршрута."""
    route = await route_crud.get(route_id, session)
    if route is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Маршрут не найден!',
        )
    return route


async def check_route_duplicate(
    session: AsyncSession,
    from_town: str,
    to_town: str,
) -> None:
    """Провверка на дублирование маршрута."""
    routes = await route_crud.get_routes_by_towns(
        session, from_town=from_town, to_town=to_town
    )
    if len(routes):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Маршрут с такими пунктами уже существует!',
        )
