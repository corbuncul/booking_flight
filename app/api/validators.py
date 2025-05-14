from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.city import city_crud
from app.crud.discount import discount_crud
from app.crud.flight import flight_crud
from app.crud.flightcity import flightcity_crud
from app.crud.passenger import passenger_crud
from app.crud.routecost import routecost_crud
from app.crud.ticket import ticket_crud
from app.models import City, Discount, Flight, FlightCity, Passenger, RouteCost, Ticket


async def check_city_exists(session: AsyncSession, city_id: int) -> City:
    """Проверка существования населенного пункта."""
    city = await city_crud.get(city_id, session)
    if city is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Населенный пункт не найден!',
        )
    return city


async def check_city_name_duplicate(
    session: AsyncSession, city_name: str
) -> None:
    """Проверка на дублирование названий населенных пунктов."""
    city = await city_crud.get_city_by_name(session=session, name=city_name)
    if city is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Населенный пункт с таким названием уже существует!',
        )


async def check_city_code_duplicate(
    session: AsyncSession, city_code: str
) -> None:
    """Проверка на дублирование кодов населенных пунктов."""
    city = await city_crud.get_city_by_code(session=session, code=city_code)
    if city is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Населенный пункт с таким кодом уже существует!',
        )


async def check_discount_exists(
    session: AsyncSession,
    discount_id: int
) -> Discount:
    """Проверка существования скидки."""
    discount = await discount_crud.get(discount_id, session)
    if discount is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Скидка не найдена!',
        )
    return discount


async def check_discount_code_dublicate(
    session: AsyncSession, discount_code: str
) -> None:
    """Проверка на дублирование скидки."""
    discount = await discount_crud.get_discount_by_code(
        session=session,
        code=discount_code
    )
    if discount is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Скидка с таким кодом уже существует!',
        )


async def check_flight_duplicate(
    session: AsyncSession,
    flight_number: str,
    flight_date: datetime,
) -> None:
    """Провверка на дублирование рейса."""
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
    """Проверка существования рейса."""
    flight = await flight_crud.get(flight_id, session)
    if flight is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Рейс не найден!'
        )
    return flight


async def check_flightcity_duplicate(
    session: AsyncSession,
    flight_id: int,
    city_id: int,
) -> None:
    """Провверка на дублирование города в рейсе."""
    flightcity_id = await flightcity_crud.get_flightcity_by_ids(
        session, flight_id, city_id
    )
    if flightcity_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такой город в данном рейсе уже существует!',
        )


async def check_flightcity_exists(
    session: AsyncSession,
    flightcity_id: int,
) -> FlightCity:
    """Проверка существования связи город - рейс."""
    flightcity = await flightcity_crud.get(
        session, flightcity_id
        )
    if flightcity is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Связи город - рейс не найдено!'
        )
    return flightcity


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


async def check_routecost_exists(
    session: AsyncSession,
    routecost_id: int,
) -> RouteCost:
    """Проверка существования маршрута."""
    route = await routecost_crud.get(routecost_id, session)
    if route is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Маршрут не найден!',
        )
    return route


async def check_routecost_duplicate(
    session: AsyncSession,
    from_city_id: int,
    to_city_id: int,
) -> None:
    """Провверка на дублирование маршрута."""
    routes = await routecost_crud.get_cost_by_cities(
        session, from_city_id=from_city_id, to_city_id=to_city_id
    )
    if len(routes):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Маршрут с такими пунктами уже существует!',
        )
