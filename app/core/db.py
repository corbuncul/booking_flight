from datetime import datetime

from sqlalchemy import Column, Integer, inspect
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    sessionmaker,
)

from app.core.config import config


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для моделей."""

    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self, exclude_none: bool = False) -> dict:
        """Преобразует объект модели в словарь.

        Args:
            exclude_none (bool): Исключать ли None значения из результата

        Returns:
            dict: Словарь с данными объекта

        """
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            if isinstance(value, datetime):
                value = value.isoformat()

            if not exclude_none or value is not None:
                result[column.key] = value

        return result


engine = create_async_engine(config.db.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
