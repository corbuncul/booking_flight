import contextlib
from datetime import date

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import config
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr,
    password: str,
    name: str,
    tg_id: int,
    tg_username: str,
    birthday: date,
    is_active: bool | None = True,
    is_superuser: bool | None = False,
    is_verified: bool | None = False,
    username: str | None = None,
    surname: str | None = None,
    phone: str | None = None
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            name=name,
                            surname=surname,
                            username=username,
                            is_superuser=is_superuser,
                            tg_id=tg_id,
                            tg_username=tg_username,
                            birthday=birthday,
                            phone=phone,
                            is_active=is_active,
                            is_verified=is_verified
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if (
        config.superuser.email is not None
        and config.superuser.password is not None
    ):
        await create_user(
            email=config.superuser.email,
            name=config.superuser.name,
            surname=config.superuser.surname,
            username=config.superuser.username,
            password=config.superuser.password.get_secret_value(),
            tg_id=config.superuser.tg_id,
            tg_username=config.superuser.tg_username,
            birthday=config.superuser.birthday,
            phone=config.superuser.phone,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
