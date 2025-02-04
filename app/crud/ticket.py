from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticket
from app.crud import CRUDBase
from app.schemas.ticket import TicketDB


class CRUDTicket(CRUDBase):

    async def get_ticket_by_number(
        self, session: AsyncSession, number: int
    ) -> Optional[TicketDB]:
        """Получение билета по номеру."""
        db_ticket = await session.execute(
            select(self.model).where(
                self.model.number == number
            )
        )
        return db_ticket.scalars().first()


ticket_crud = CRUDTicket(Ticket)
