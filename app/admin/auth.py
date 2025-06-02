import contextlib
from typing import AsyncGenerator, Optional, Tuple

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqladmin.authentication import AuthenticationBackend

from app.core.config import config
from app.core.logger import logger
from app.core.db import get_async_session
from app.core.user import UserManager, get_jwt_strategy, get_user_db
from app.models import User


class AdminAuth(AuthenticationBackend):
    """Аутентификация для административного интерфейса."""

    def __init__(self) -> None:
        """Метод инициализации класса AdminAuth."""
        super().__init__(secret_key=config.app.secret_key.get_secret_value())
        self.jwt_strategy = get_jwt_strategy()

    @contextlib.asynccontextmanager
    async def get_user_manager(self) -> AsyncGenerator[UserManager, None]:
        """Метод получения кастомного менеджера пользователей."""
        async for session in get_async_session():
            async for user_db in get_user_db(session):
                yield UserManager(user_db)

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Tuple[Optional[User], Optional[str]]:
        """Аутентификация пользователя по имени пользователя и паролю."""
        async with self.get_user_manager() as user_manager:
            credentials = OAuth2PasswordRequestForm(
                username=username,
                password=password,
            )
            user = await user_manager.authenticate(credentials)
            if user and user.is_active:
                token = await self.jwt_strategy.write_token(user)
                logger.info('User %s authenticate.', user)
                return user, token
            return None, None

    async def login(self, request: Request):
        form = await request.form()
        username = form["username"]
        password = form["password"]

        user, token = await self.authenticate_user(username, password)
        if user and user.is_superuser:
            request.session.update({"access_token": token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Обработка выхода администратора."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверка аутентификации администратора."""
        token = request.session.get('access_token')
        if not token:
            return False
        try:
            async with self.get_user_manager() as user_manager:
                user = await self.jwt_strategy.read_token(token, user_manager)
                if user is None:
                    logger.info('попытка входа.')
                    return False
                if user and user.is_superuser:
                    logger.info('Пользователь %s вошел.', user)
                    return True
                return False
        except Exception as e:
            logger.error('Ошибка %s', e)
            return False
