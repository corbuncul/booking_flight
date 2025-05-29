from typing import Optional

from fastapi_users.password import PasswordHelper
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.config import config
from app.core.init_db import get_async_session_context, get_user_db_context
from app.core.logger import logger


class AdminAuth(AuthenticationBackend):
    """Аутентификация для административного интерфейса."""

    def __init__(self):
        try:
            secret_key = config.app.secret_key.get_secret_value()
            super().__init__(secret_key=secret_key)
            self.password_helper = PasswordHelper()
            logger.info("AdminAuth initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AdminAuth: {e}")
            raise

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")  # форма отправляет как username
        password = form.get("password")

        if not email or not password:
            logger.warning("Login attempt without email or password")
            return False

        try:
            async with get_async_session_context() as session:
                async with get_user_db_context(session) as user_db:
                    # Получаем пользователя по email
                    user = await user_db.get_by_email(email)

                    if not user:
                        logger.warning(f"User not found: {email}")
                        return False

                    if not user.is_superuser:
                        logger.warning(f"Non-superuser login attempt: {email}")
                        return False

                    # Проверяем пароль
                    valid_password = self.password_helper.verify_password(
                        password, user.hashed_password
                    )
                    if not valid_password:
                        logger.warning(f"Invalid password for user: {email}")
                        return False

                    logger.info(f"Successful login: {email}")
                    request.session.update({"admin_user": email})
                    return True

        except Exception as e:
            logger.error(f"Login error for {email}: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        try:
            admin_user = request.session.get("admin_user")
            request.session.pop("admin_user", None)
            logger.info(f"User logged out: {admin_user}")
            return True
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        try:
            admin_user = request.session.get("admin_user")
            if not admin_user:
                logger.debug("No admin_user in session")
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
            logger.debug(f"Authenticated: {admin_user}")
            return None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
