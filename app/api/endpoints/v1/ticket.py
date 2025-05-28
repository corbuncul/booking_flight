from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_ticket_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import passenger_crud, routecost_crud, ticket_crud
from app.schemas import TicketCreate, TicketDB, TicketResponse
from app.services.discount import apply_discount

router = APIRouter()


@router.get(
    '/',
    response_model=list[TicketDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_tickets(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех билетов. Только для суперюзеров."""
    return await ticket_crud.get_all(session)


@router.post(
    '/',
    response_model=TicketDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_ticket(
    ticket: TicketCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание билета."""
    ticket_in = ticket.model_dump()
    passenger = await passenger_crud.get(ticket_in['id'], session)
    discount_code = ''
    today = date.today()
    age = relativedelta(today, passenger.birthday)
    if age.years < 2:
        discount_code = 'РМГ'
    elif age.years < 12:
        discount_code = 'РБГ'
    original_price = await routecost_crud.get_cost_by_cities(
        session,
        from_city_id=ticket_in['from_city_id'],
        to_city_id=ticket_in['to_city_id']
    )
    final_price = await apply_discount(session, discount_code, original_price.cost)
    ticket.discount_code = discount_code
    ticket.final_price = final_price
    new_ticket = await ticket_crud.create(ticket, session)
    return new_ticket


@router.get(
    '/{ticket_id}',
    response_model=TicketDB,
    dependencies=[Depends(current_superuser)],
)
async def get_ticket(
    ticket_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение билета по id."""
    ticket = await check_ticket_exists(session, ticket_id)
    return ticket


@router.get(
    '/by_number/{ticket_number}',
    response_model=TicketResponse,
    dependencies=[Depends(current_superuser)],
)
async def get_ticket_by_number(
    ticket_number: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение билета по номеру."""
    ticket = await ticket_crud.get_ticket_by_number(session, ticket_number)
    return ticket


@router.get(
    '/by_date_flight/{date_flight}',
    response_model=list[TicketResponse],
    dependencies=[Depends(current_superuser)],
)
async def get_ticket_by_date_flight(
    date_flight: date,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение билетов по дате вылета."""
    tickets = await ticket_crud.get_tickets_by_date_flight(
        session, date_flight
    )
    return tickets


@router.get(
    '/by_flight_id/{flight_id}',
    response_model=list[TicketResponse],
    dependencies=[Depends(current_superuser)],
)
async def get_ticket_by_flight(
    flight_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение билетов по рейсу."""
    tickets = await ticket_crud.get_tickets_by_flight(session, flight_id)
    return tickets


@router.delete(
    '/{ticket_id}',
    response_model=TicketDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_passenger(
    ticket_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление билета."""
    ticket = await check_ticket_exists(session, ticket_id)
    db_ticket = await ticket_crud.remove(ticket, session)
    return db_ticket
