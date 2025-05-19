from fastapi import APIRouter

from .city import router as city_router
from .discount import router as discount_router
from .flight import router as flight_router
from .flightcity import router as flightcity_router
from .routecost import router as routecost_router
from .user import router as user_router
from .passenger import router as passenger_router
from .ticket import router as ticket_router

router_v1 = APIRouter()
router_v1.include_router(
    city_router,
    prefix='/city',
    tags=['Населенные пункты'],
)
router_v1.include_router(
    discount_router, prefix='/discount', tags=['Скидки']
)
router_v1.include_router(
    flight_router,
    prefix='/flight',
    tags=['Рейсы'],
)
router_v1.include_router(
    flightcity_router, prefix='/flightcity', tags=['Города в рейсах']
)
router_v1.include_router(
    routecost_router, prefix='/routecost', tags=['Цены']
)
router_v1.include_router(
    passenger_router,
    prefix='/passenger',
    tags=['Пассажиры'],
)
router_v1.include_router(
    ticket_router,
    prefix='/ticket',
    tags=['Билеты'],
)
router_v1.include_router(user_router)
