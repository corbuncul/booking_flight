from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_ticket_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import ticket_crud
from app.schemas.ticket import (
    TicketCreate,
    TicketDB
)

router = APIRouter()


@router.get(
    '/',
    response_model=TicketDB,
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
    """Получение билета."""
    ticket = await check_ticket_exists(session, ticket_id)
    return ticket


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
