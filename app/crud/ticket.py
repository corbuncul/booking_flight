from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Ticket
from app.crud import CRUDBase
from app.schemas.ticket import TicketDB


class CRUDTicket(CRUDBase):
    """Класс для CRUD модели Ticket."""

    async def get_ticket_by_number(
        self, session: AsyncSession, number: int
    ) -> TicketDB | None:
        """Получение билета по номеру."""
        db_ticket = await session.execute(
            select(self.model).where(self.model.number == number)
        )
        return db_ticket.scalars().first()

    async def get_tickets_by_flight(
        self, session: AsyncSession, flight_id: int
    ) -> list[TicketDB | None]:
        """Получение билетов по id полета."""
        db_ticket = await session.execute(
            select(self.model).where(self.model.flight_id == flight_id)
        )
        return db_ticket.scalars().all()

    async def get_tickets_by_date_flight(
        self, session: AsyncSession, date_flight: datetime
    ) -> list[TicketDB | None]:
        """Получение билетов по дате вылета."""
        db_ticket = await session.execute(
            select(self.model)
            .options(joinedload(self.model.flight))
            .where(self.model.flight.date_flight == date_flight)
        )
        return db_ticket.scalars().all()


ticket_crud = CRUDTicket(Ticket)
