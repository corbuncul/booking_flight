from telegram import (
    InlineKeyboardMarkup,
)


from app.bot.keyboard_buttons import (
    get_inl_cities_buttons,
    get_inl_flights_buttons,
    inline_about_project,
    inline_about_project_not_reg,
    inline_back_to_main_menu,
    inline_booking,
    inline_flights,
    inline_cities,
    inline_exit_app,
)
from app.bot.paginations import create_objects_paginator


def main_keyboard_inl() -> InlineKeyboardMarkup:
    """Встроенная клавиатура основной клавиатуры."""
    keyboard = [
        inline_booking,
        inline_flights,
        inline_cities,
    ]
    keyboard.append(inline_about_project)
    keyboard.append(inline_exit_app)
    return InlineKeyboardMarkup.from_column(keyboard)


def not_registred_user_keyboard_inl() -> InlineKeyboardMarkup:
    """Встроенная клавиатура незарегистрированного пользователя."""
    keyboard = [[
        inline_about_project_not_reg,
    ]]
    return InlineKeyboardMarkup(keyboard)


def to_main_menu_keyboard_inl() -> InlineKeyboardMarkup:
    """Встроенная клавиатура.

    Клавиатура с кнопками:
    - "В главное меню".
    """
    keyboard = [[
        inline_back_to_main_menu,
    ]]
    return InlineKeyboardMarkup(keyboard)


def cities_search_result_keyboard_inl(
        page_count: int,
        current_page: int,
        callback_data_next: str,
        callback_data_previous: str,
        cities: list[dict] = [],
) -> InlineKeyboardMarkup:
    """Создаёт inline-клавиатуру для городов."""
    keyboard = [
        [button] for button in get_inl_cities_buttons(cities)
    ]
    pagination_block = create_objects_paginator(
        page_count=page_count,
        current_page=current_page,
        callback_data_next=callback_data_next,
        callback_data_previous=callback_data_previous,
    )
    keyboard.append(pagination_block)
    keyboard.append([inline_back_to_main_menu])
    return InlineKeyboardMarkup(keyboard)


def flights_search_result_keyboard_inl(
        page_count: int,
        current_page: int,
        callback_data_next: str,
        callback_data_previous: str,
        flights: list[dict] = [],
) -> InlineKeyboardMarkup:
    """Создаёт inline-клавиатуру для рейсов."""
    keyboard = [
        [button] for button in get_inl_flights_buttons(flights)
    ]
    pagination_block = create_objects_paginator(
        page_count=page_count,
        current_page=current_page,
        callback_data_next=callback_data_next,
        callback_data_previous=callback_data_previous,
    )
    keyboard.append(pagination_block)
    keyboard.append([inline_back_to_main_menu])
    return InlineKeyboardMarkup(keyboard)
