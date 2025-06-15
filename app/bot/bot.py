from telegram.ext import (
    Application,
    CommandHandler
)

from app.bot.handlers import (
    about_project_not_reg_handler,
    common_conversation_handler
)
from app.core.config import config

bot = Application.builder().token(config.bot.token.get_secret_value()).build()

bot.add_handler(common_conversation_handler)
bot.add_handler(about_project_not_reg_handler)
