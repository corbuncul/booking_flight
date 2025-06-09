from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import connection
from app.crud import passenger_crud
from app.core.logger import logger
from app.schemas import (
    CityDB,
    DiscountDB,
    FlightCities,
    FlightCityDB,
    FlightDB,
    PassengerCreate,
    PassengerDB,
    PassengerTickets,
    TicketCreate,
    TicketDB,
    TicketResponse
)
from app.bot.keyboards.kbd import main_keyboard, booking_keyboard

router = Router()


@router.message(CommandStart())
@connection()
async def cmd_start(message: Message, session: AsyncSession, **kwargs):
    try:
        user_id = message.from_user.id
        user = await passenger_crud.find_one_or_none(
            session=session, tg_id=user_id
        )
        welcome_text = 'Добро пожаловать'
        if user:
            username = f'{user.name} {user.surname}'
            welcome_text += f', {username}'
        welcome_text += (
            '!\n\n'
            'Здесь вы сможете:\n\n'
            '  Записаться на рейс\n\n'
            '  Посмотреть информацию по рейсам\n\n'
            '  Посмотреть информацию по населенным пунктам.\n\n'
        )

        await message.answer(welcome_text, reply_markup=main_keyboard())

    except Exception as e:
        logger.error('Ошибка: %s', e)
        await message.answer(
            'Произошла ошибка. Пожалуйста, попробуйте снова позже.'
        )


@router.callback_query(F.data == 'booking')
@connection()
async def get_user_rating(call: CallbackQuery, session: AsyncSession, **kwargs):
    await call.answer()
    await call.message.delete()
    text = 'Введите Имя, Фамилию, дату рождения, номер документа, дату рейса, откуда и куда.'
    await call.message.answer(text, reply_markup=booking_keyboard())
