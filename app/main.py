from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.endpoints.v1.common import router as router_v1
from app.core.config import config
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
app_v1 = FastAPI(
    title='Booking Flight v1',
    description='Бронирование билетов. Версия API v1.'
)

app_v1.include_router(router_v1)

app.mount('/v1', app_v1)
