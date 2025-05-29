from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from app.admin.auth import AdminAuth
from app.admin.base import (
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
from app.core.config import config
from app.core.db import engine
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(
    title=config.app.title,
    description=config.app.description,
    lifespan=lifespan,
)

# Инициализация административного интерфейса
authentication_backend = AdminAuth()
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="Администрирование",
    logo_url=None,
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
    title="Booking Flight v1", description="Бронирование билетов. Версия API v1."
)

app_v1.include_router(router_v1)
app.mount("/v1", app_v1)
