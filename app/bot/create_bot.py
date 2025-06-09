from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import config
from app.core.logger import logger

if config.bot.token.get_secret_value() is not None:
    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
else:
    logger.error('Токен пуст, бот не запущен.')


async def start_bot():
    try:
        for admin_id in config.superuser.tg_id:
            await bot.send_message(
                admin_id, f'Бот "{config.bot.name}" запущен.'
            )
    except Exception as e:
        logger.error('Ошибка запуска бота: %s', e)


async def stop_bot():
    try:
        for admin_id in config.superuser.tg_id:
            await bot.send_message(
                admin_id, f'Бот "{config.bot.name}" остановлен.'
            )
    except Exception as e:
        logger.error('Ошибка остановки бота: %s', e)
