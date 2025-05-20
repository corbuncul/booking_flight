from typing import Any, Generic, Optional, TypeVar, Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

T = TypeVar("T", bound=Base)


class CRUDBase(Generic[T]):
    """Базовый класс для всех CRUD."""

    def __init__(self, model: type[T]) -> None:
        """Конструктор объекта класса CRUDBase."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[T]:
        """Получение одного объекта по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ) -> Optional[T]:
        """Получение объекта по указанному атрибуту."""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value),
        )
        return db_obj.scalars().first()

    async def find_one_or_none(
        self,
        session: AsyncSession,
        **filter_by: Any,
    ) -> Optional[T]:
        """Поиск одного объекта по фильтру, либо None, если не найден."""
        db_obj = await session.execute(
            select(self.model).filter_by(**filter_by),
        )
        return db_obj.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> Sequence[T]:
        """Получение всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession,
        user: User | None = None
    ) -> T:
        """Создание объекта."""
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: T,
        obj_in: BaseModel,
        session: AsyncSession,
    ) -> T:
        """Обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: T,
        session: AsyncSession,
    ) -> T:
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
