from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.validators import (
    check_queue_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import queue_crud
from app.schemas.queue import (
    QueueCreate,
    QueueDB
)

router = APIRouter()


@router.get(
    '/',
    response_model=QueueDB,
    dependencies=[Depends(current_superuser)],
)
async def get_all_queues(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех записей. Только для суперюзеров."""
    return await queue_crud.get_all(session)


@router.post(
    '/',
    response_model=QueueDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_queue(
    queue: QueueCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание записи."""
    new_queue = await queue_crud.create(queue, session)
    return new_queue


@router.delete(
    '/{queue_id}',
    response_model=QueueDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_passenger(
    queue_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление записи."""
    queue = await check_queue_exists(session, queue_id)
    db_queue = await queue_crud.remove(queue, session)
    return db_queue
