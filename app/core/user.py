from collections.abc import AsyncGenerator
from typing import Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    exceptions,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import config
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

LIFETIME = 3600
PASSWORD_MIN_LENGHT = 3

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator:
    """Функция возвращает генератор пользователя из БД."""
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Класс менеджера пользователей."""

    def __init__(
        self,
        user_db: SQLAlchemyUserDatabase,
        user: Optional[User] = None,
    ) -> None:
        """Конструктор объекта класса UserManager."""
        super().__init__(user_db)
        self.user = user

    @property
    def db_session(self) -> AsyncSession:
        """Функция возвращает асинхронную сессию для работы с БД."""
        return self.user_db.session

    async def authenticate(
        self,
        credentials: OAuth2PasswordRequestForm,
    ) -> Optional[User]:
        """Функция авторизации."""
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = (
            self.password_helper.verify_and_update(
                credentials.password,
                user.hashed_password,
            )
        )
        if not verified:
            return None
        if updated_password_hash is not None:
            await self.user_db.update(
                user,
                {'hashed_password': updated_password_hash},
            )

        return user

    async def get_by_username(self, username: str) -> User | None:
        """Функция возвращает пользователя по указанному username."""
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        result = result.scalars().one_or_none()
        if result is None:
            raise exceptions.UserNotExists('Такого пользователя нет в базе')
        return result

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        if len(password) < PASSWORD_MIN_LENGHT:
            raise InvalidPasswordException(
                reason=(
                    'Password should be at least '
                    f'{PASSWORD_MIN_LENGHT} characters'
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(
    user_db: AsyncSession = Depends(get_user_db),
) -> AsyncGenerator:
    """Функция возвращает генератор менеджера пользователей."""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Функция возвращает стратегию JWT-токена."""
    return JWTStrategy(
        secret=config.app.secret_key.get_secret_value(),
        lifetime_seconds=LIFETIME
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
