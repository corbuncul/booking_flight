from fastapi import APIRouter

from . import (
    city_router, discount_router, flight_router,
    flightcity_router, routecost_router, passenger_router,
    ticket_router, user_router
)

router = APIRouter()
router.include_router(
    city_router,
    prefix='/city',
    tags=['Населенные пункты'],
)
router.include_router(
    discount_router, prefix='/discount', tags=['Скидки']
)
router.include_router(
    flight_router,
    prefix='/flight',
    tags=['Рейсы'],
)
router.include_router(
    flightcity_router, prefix='/flightcity', tags=['Города в рейсах']
)
router.include_router(
    routecost_router, prefix='/routecost', tags=['Цены']
)
router.include_router(
    passenger_router,
    prefix='/passenger',
    tags=['Пассажиры'],
)
router.include_router(
    ticket_router,
    prefix='/ticket',
    tags=['Билеты'],
)
router.include_router(user_router)
