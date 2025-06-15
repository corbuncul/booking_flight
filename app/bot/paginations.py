from telegram import InlineKeyboardButton

from app.bot.keyboard_buttons import inline_no_action


def create_objects_paginator(
    page_count: int,
    current_page: int,
    callback_data_next: str,
    callback_data_previous: str,
) -> list:
    """Создаёт пагинатор для списка объектов."""
    pagination_block = []
    if current_page == 1 and page_count > 1:
        pagination_block.append(inline_no_action)
    if current_page > 1:
        pagination_block.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=callback_data_previous,
            ),
        )
    if page_count > 1:
        pagination_block.append(
            InlineKeyboardButton(
                text=f"Страница {current_page} / {page_count}",
                callback_data="current_page",
            ),
        )
    if current_page < page_count:
        pagination_block.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=callback_data_next,
            ),
        )
    if current_page == page_count and page_count > 1:
        pagination_block.append(inline_no_action)
    return pagination_block
