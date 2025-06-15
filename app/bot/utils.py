from typing import Any, Dict, Optional

import aiohttp
import redis
from telegram import Message, Update

from app.bot.keyboads import (
    main_keyboard_inl,
    not_registred_user_keyboard_inl,
    to_main_menu_keyboard_inl,
)
from app.core.config import config
from app.core.constants import PAGINATION_LIMIT


redis_client = redis.Redis(
    host=config.redis.host,
    port=config.redis.port,
    db=config.redis.db,
    decode_responses=True,
    encoding='utf-8',
)


async def get_bot_token() -> str:
    token = redis_client.get('bot_token')

    if not token:
        username = config.superuser.username
        password = config.superuser.password.get_secret_value()
        data = dict(username=username, password=password)

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=f'{config.app.host}/auth/jwt/login',
                data=data,
            )

        result = await response.json(content_type=None)
        token = result['access_token']
        redis_client.set('bot_token', token, ex=3599)

    return token


async def free_text_reply(update: Update) -> None:
    """Заглушка для свободного текста."""
    if isinstance(update.effective_message, Message):
        await update.effective_message.reply_text(
            text="Обработка свободного текста не осуществляется.",
            reply_markup=to_main_menu_keyboard_inl(),
        )


async def under_development_reply(update: Update) -> None:
    """Заглушка для разрабатываемого раздела."""
    if isinstance(update.effective_message, Message):
        await update.effective_message.reply_text(
            text="Этот раздел в разработке",
            reply_markup=to_main_menu_keyboard_inl(),
        )


async def non_registred_reply(update: Update) -> None:
    """Ответ незарегистрированному пользователю."""
    if isinstance(update.effective_message, Message):
        await update.effective_message.reply_text(
            text=(
                f"Привет, {update.effective_user.full_name}! 👋\n"
                f"Для продолжения работы необходимо зарегистрироваться!\n"
                f"Пожалуйста, обратитесь к администратору"
            ),
            reply_markup=not_registred_user_keyboard_inl(),
        )


async def about_project(update: Update) -> None:  # noqa: D103
    """Вывод базовой информации о приложении."""
    await update.callback_query.edit_message_reply_markup(None)
    await update.callback_query.answer()
    if isinstance(update.effective_message, Message):
        await update.effective_message.reply_text(
            text=config.app.title,
            reply_markup=to_main_menu_keyboard_inl(),
        )

