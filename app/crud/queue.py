from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Queue
from app.crud import CRUDBase
from app.schemas.queue import QueueDB


class CRUDQueue(CRUDBase):

    async def get_queue_by_flight(
        self, session: AsyncSession, flight: int
    ) -> Optional[QueueDB]:
        """Получение очереди по id вылета."""
        db_queue = await session.execute(
            select(self.model).where(
                self.model.flight == flight
            )
        )
        return db_queue.scalars().first()


queue_crud = CRUDQueue(Queue)
