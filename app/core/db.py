from datetime import datetime
from functools import wraps

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    sessionmaker
)

from app.core.config import config


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для моделей."""

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        # CamelCase -> snake_case
        name = cls.__name__[0].lower() + cls.__name__[1:]
        name = ''.join(
            ['_' + c.lower() if c.isupper() else c for c in name]
        ).lstrip('_')
        return name

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


def connection():
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with AsyncSessionLocal() as session:
                try:
                    return await method(*args, session=session, **kwargs)
                except Exception as e:
                    await session.rollback()
                    raise e
                finally:
                    await session.close()

        return wrapper
    return decorator
