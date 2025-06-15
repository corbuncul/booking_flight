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
    user = update.effective_user
    if update.callback_query:
        await update.callback_query.edit_message_reply_markup(None)
        await update.callback_query.answer()
    if isinstance(user, User):
        user_status = await get_user_status(tg_id=user.id)
        is_user_registred = user_status.get('is_registered')
        if is_user_registred:
            await greet_registred_user(
                update=update,
                is_user_admin=user_status.get('is_admin'),
                is_user_subscribed=user_status.get('is_subscribed'),
            )
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


async def free_text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Заглушка для свободного текста."""
    await free_text_reply(update=update)


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
                check_vacancy_text_callback,
            ),
        ],
        FLIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                find_colleagues_in_db_callback,
            ),
        ],
        CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                find_colleagues_in_db_callback,
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
