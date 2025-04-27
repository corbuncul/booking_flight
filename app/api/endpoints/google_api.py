from datetime import timedelta
from typing import Union

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import (
    city_crud,
    flight_crud,
    passenger_crud,
    route_crud,
    ticket_crud
)
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)
from app.schemas.city import CityDB
from app.schemas.flight import FlightDB
from app.schemas.passenger import PassengerDB
from app.schemas.route import RouteDB
from app.schemas.ticket import TicketDB

router = APIRouter()


@router.get(
    '/passengers',
    response_model=list[PassengerDB],
    dependencies=[Depends(current_superuser)],
)
async def get_passengers(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, Union[str, timedelta]]]:
    """Только для суперюзеров. Список всех пассажиров."""
    passengers = await passenger_crud.get_all(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, passengers, wrapper_services
    )
    return passengers


@router.get(
    '/tickets',
    response_model=list[TicketDB],
    dependencies=[Depends(current_superuser)],
)
async def get_tickets(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, Union[str, timedelta]]]:
    """Только для суперюзеров. Список всех билетов."""
    tickets = await ticket_crud.get_all(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, tickets, wrapper_services
    )
    return tickets


@router.get(
    '/flight',
    response_model=list[FlightDB],
    dependencies=[Depends(current_superuser)],
)
async def get_flights(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, Union[str, timedelta]]]:
    """Только для суперюзеров. Список всех вылетов."""
    flights = await flight_crud.get_all(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, flights, wrapper_services
    )
    return flights


@router.get(
    '/routes',
    response_model=list[RouteDB],
    dependencies=[Depends(current_superuser)],
)
async def get_routes(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, Union[str, timedelta]]]:
    """Только для суперюзеров. Список всех маршрутов."""
    routes = await route_crud.get_all(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, routes, wrapper_services
    )
    return routes


# @router.get(
#     '/queues',
#     response_model=list[QueueDB],
#     dependencies=[Depends(current_superuser)],
# )
# async def get_queues(
#     session: AsyncSession = Depends(get_async_session),
#     wrapper_services: Aiogoogle = Depends(get_service),
# ) -> list[dict[str, Union[str, timedelta]]]:
#     """Только для суперюзеров. Очередь."""
#     queues = await queue_crud.get_all(
#         session
#     )
#     spreadsheetid = await spreadsheets_create(wrapper_services)
#     await set_user_permissions(spreadsheetid, wrapper_services)
#     await spreadsheets_update_value(
#         spreadsheetid, queues, wrapper_services
#     )
#     return queues
