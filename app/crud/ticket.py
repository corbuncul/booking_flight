from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Ticket
from app.crud import CRUDBase


class CRUDTicket(CRUDBase[Ticket]):
    """Класс для CRUD модели Ticket."""

    model = Ticket

    async def get_ticket_by_number(
        self, session: AsyncSession, number: str
    ) -> Ticket | None:
        """Получение билета по номеру."""
        db_ticket = await session.execute(
            select(self.model)
            .options(
                selectinload(self.model.flight),
                selectinload(self.model.passenger),
                selectinload(self.model.to_city),
                selectinload(self.model.from_city)
            ).where(self.model.number == number)
        )
        return db_ticket.scalars().first()

    async def get_tickets_by_flight(
        self, session: AsyncSession, flight_id: int
    ) -> Sequence[Ticket] | None:
        """Получение билетов по id полета."""
        db_ticket = await session.execute(
            select(self.model)
            .options(
                selectinload(self.model.flight),
                selectinload(self.model.passenger),
                selectinload(self.model.to_city),
                selectinload(self.model.from_city)
            ).where(self.model.flight_id == flight_id)
        )
        return db_ticket.scalars().all()

    async def get_tickets_by_date_flight(
        self, session: AsyncSession, date_flight: date
    ) -> Sequence[Ticket] | None:
        """Получение билетов по дате вылета."""
        db_ticket = await session.execute(
            select(self.model)
            .options(
                selectinload(self.model.flight),
                selectinload(self.model.passenger),
                selectinload(self.model.to_city),
                selectinload(self.model.from_city)
            ).where(self.model.flight.date_flight == date_flight)
        )
        return db_ticket.scalars().all()


ticket_crud = CRUDTicket()
