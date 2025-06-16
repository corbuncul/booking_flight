from typing import Any, Dict, Optional

import aiohttp
import redis
from telegram import Message, Update

from app.bot.keyboads import (
    cities_search_result_keyboard_inl,
    create_objects_paginator,
    flights_search_result_keyboard_inl,
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


async def greet_registred_user(
    update: Update,
) -> None:
    """Приветствие зарегистрированного пользователя."""
    if isinstance(update.effective_message, Message):
        await update.effective_message.reply_text(
            text=f"Добро пожаловать, {update.effective_user.full_name}! 👋",
            reply_markup=main_keyboard_inl(),
        )


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


# async def get_city_from_db(
#     city_id: int,
# ) -> Optional[Dict[str, Any]]:
#     """Получение данных города из базы данных."""
#     token = await get_bot_token()
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(
#             url=f'{config.app.host}/city/{city_id}',
#             headers=dict(
#                 accept='application/json',
#                 Authorization=f'Bearer {token}',
#             ),
#         )
#     return await response.json(content_type=None)


async def get_obj_from_db(
    obj_id: int,
    obj_str: str
) -> Optional[Dict[str, Any]]:
    """Получение данных объеста из базы данных."""
    token = await get_bot_token()
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=f'{config.app.host}/{obj_str}/{obj_id}',
            headers=dict(
                accept='application/json',
                Authorization=f'Bearer {token}',
            ),
        )
    return await response.json(content_type=None)


async def find_flights_in_db(
    update: Update,
) -> None:
    """Получение списка полетов."""
    token = await get_bot_token()
    query = update.callback_query
    result_page = 1
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=f'{config.app.host}/flight',
            headers=dict(
                accept='application/json',
                Authorization=f'Bearer {token}',
            ),
        )
    if response.status == 403:
        return await non_registred_reply(update)
    result = await response.json(content_type=None)
    flights = result.get('items', None)
    page_count = result.get('pages', 1)
    result_text = 'Выберите рейс:' if flights else 'Рейсы не найдены'
    reply_markup = flights_search_result_keyboard_inl(
        page_count=page_count,
        current_page=result_page,
        callback_data_next=f'flightspage_{result_page+1}',
        callback_data_previous=f'flightspage_{result_page-1}',
        flights=flights
    )
    if query:
        await query.edit_message_reply_markup(
            reply_markup=reply_markup,
        )
    else:
        await update.effective_message.reply_text(
            text=result_text,
            reply_markup=reply_markup,
        )


async def find_cities_in_db(
    update: Update,
) -> None:
    """Получение списка городов."""
    token = await get_bot_token()
    query = update.callback_query
    result_page = 1
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=f'{config.app.host}/city',
            headers=dict(
                accept='application/json',
                Authorization=f'Bearer {token}',
            ),
        )
    if response.status == 403:
        return await non_registred_reply(update)
    result = await response.json(content_type=None)
    cities = result.get('items', None)
    page_count = result.get('pages', 1)
    result_text = 'Выберите населенный пункт:' if cities else 'населенные пункты не найдены'
    reply_markup = cities_search_result_keyboard_inl(
        page_count=page_count,
        current_page=result_page,
        callback_data_next=f'citiespage_{result_page+1}',
        callback_data_previous=f'citiesspage_{result_page-1}',
        cities=cities
    )
    if query:
        await query.edit_message_reply_markup(
            reply_markup=reply_markup,
        )
    else:
        await update.effective_message.reply_text(
            text=result_text,
            reply_markup=reply_markup,
        )
