from telegram.ext import (
    Application,
    CommandHandler
)

from app.bot.handlers import (
    start,
    help_handler
)
from app.core.config import config

bot = Application.builder().token(config.bot.token.get_secret_value()).build()

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help_handler))
