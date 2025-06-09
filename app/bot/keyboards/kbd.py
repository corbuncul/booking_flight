from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Запись на самолет', callback_data='booking')
    kb.button(text='Рейсы', callback_data='flights')
    kb.button(text='Населенные пункты', callback_data="cities")
    kb.adjust(1)
    return kb.as_markup()


def booking_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Запись на самолет', callback_data='booking')
    kb.button(text='Рейсы', callback_data='flights')
    kb.button(text='Населенные пункты', callback_data="cities")
    kb.adjust(1)
    return kb.as_markup()
