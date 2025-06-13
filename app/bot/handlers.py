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
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)


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
