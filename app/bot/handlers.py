from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)

from app.core.config import config
from app.bot.utils import (
    about_project,
    get_obj_from_db,
    create_objects_paginator,
    find_cities_in_db,
    find_flights_in_db,
    free_text_reply,
    get_obj_from_db,
    greet_registred_user,
    non_registred_reply,
    under_development_reply,
)

SELECT, BOOKING, FLIGHT, CITY = range(4)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показ подсказки"""
    await update.message.reply_text(
        'Используйте /booking или /flights или /cities '
        'для записи на рейс, просмотр рейсов или просмотр нас. пунктов.'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        'Вас приветствует бот для записи на самолет. '
        'Используйте /booking или /flights или /cities '
        'для записи на рейс, просмотр рейсов или просмотр нас. пунктов.'
    )


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Отправка сообщения на команду /start."""
    if update.callback_query:
        await update.callback_query.edit_message_reply_markup(None)
        await update.callback_query.answer()
        await greet_registred_user(update=update)
        return SELECT
    await non_registred_reply(update=update)
    return 0


async def cmd_exit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Завершает диалог и закрывает сессию пользователя."""
    if update.callback_query:
        await update.callback_query.edit_message_reply_markup(None)
        await update.callback_query.answer()
    await update.effective_chat.send_message(
        text='Работа с приложннием закончена. \n'
        'Для возобновления введите /start',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def about_project_not_reg_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Вывод базовой информации о приложении."""
    await update.effective_chat.send_message(
        text=(f'{config.app.title}\n'
              f' Для начала работы введите /start'),
        reply_markup=ReplyKeyboardRemove(),
    )


async def about_project_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Вывод базовой информации о приложении."""
    await about_project(update)


async def get_cities_from_db_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Вывод списка городов."""
    await find_cities_in_db(update=update)
    return CITY


async def get_flights_from_db_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Вывод списка рейсов."""
    await find_flights_in_db(update=update)
    return FLIGHT


async def free_text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Заглушка для свободного текста."""
    await free_text_reply(update=update)


async def booking_start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Начало записи на рейс."""
    await under_development_reply(update=update)
    return SELECT


cmd_start_handler = CommandHandler(
    command='start',
    callback=start_command,
)
cmd_exit_handler = CommandHandler(
    command='exit',
    callback=cmd_exit,
)
about_project_handler = CallbackQueryHandler(
    callback=about_project_callback,
    pattern='about_project',
)
about_project_not_reg_handler = CallbackQueryHandler(
    callback=about_project_not_reg_callback,
    pattern='about_project_not_reg',
)
to_main_menu_handler = CallbackQueryHandler(
    callback=start_command,
    pattern='to_main_menu',
)
exit_app_handler = CallbackQueryHandler(
    callback=cmd_exit,
    pattern='exit_app',
)

common_conversation_handler = ConversationHandler(
    entry_points=[cmd_start_handler],
    states={
        SELECT: [],
        BOOKING: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                booking_start_callback,
            ),
        ],
        FLIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_flights_from_db_callback,
            ),
        ],
        CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_cities_from_db_callback,
            ),
        ]
    },
    fallbacks=[
        about_project_handler,
        cmd_exit_handler,
        exit_app_handler,
        to_main_menu_handler,
    ],
)
