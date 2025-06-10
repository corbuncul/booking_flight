from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin
from telegram import Update

from app.admin.auth import AdminAuth
from app.admin.admin import (
    CityAdmin,
    DiscountAdmin,
    FlightAdmin,
    FlightCityAdmin,
    PassengerAdmin,
    RouteCostAdmin,
    TicketAdmin,
    UserAdmin,
)
from app.api.endpoints.v1.common import router as router_v1
from app.bot.bot import bot
from app.core.config import config
from app.core.db import engine
from app.core.init_db import create_first_superuser
from app.core.logger import logger
from app.views.booking import router as booking_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Функция, выполняющаяся при запуске FastAPI."""
    await create_first_superuser()
    logger.info('Starting bot setup...')
    await bot.initialize()
    await bot.start()
    logger.info('Starting Telegram bot polling...')
    await bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    yield
    logger.info('Stoping bot...')
    await bot.stop()


app = FastAPI(
    title=config.app.title,
    description=config.app.description,
    lifespan=lifespan,
)

admin = Admin(
    app,
    engine,
    authentication_backend=AdminAuth(),
    title='Администрирование',
)

# Добавление всех моделей в админку
admin.add_view(CityAdmin)
admin.add_view(DiscountAdmin)
admin.add_view(FlightAdmin)
admin.add_view(FlightCityAdmin)
admin.add_view(PassengerAdmin)
admin.add_view(RouteCostAdmin)
admin.add_view(TicketAdmin)
admin.add_view(UserAdmin)

app_v1 = FastAPI(
    title='Booking Flight v1',
    description='Бронирование билетов. Версия API v1.'
)

app_v1.include_router(router_v1)
app.mount('/v1', app_v1)
app.include_router(
    booking_router,
    prefix='/booking',
    tags=['Бронирование'],
)
