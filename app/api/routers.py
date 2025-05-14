from fastapi import APIRouter

from app.api.endpoints import (
    city_router,
    discount_router,
    flight_router,
    flightcity_router,
    passenger_router,
    routecost_router,
    ticket_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    city_router,
    prefix='/city',
    tags=['Населенные пункты'],
)
main_router.include_router(
    discount_router, prefix='/discount', tags=['Скидки']
)
main_router.include_router(
    flight_router,
    prefix='/flight',
    tags=['Рейсы'],
)
main_router.include_router(
    flightcity_router, prefix='/flightcity', tags=['Города в рейсах']
)
main_router.include_router(
    routecost_router, prefix='/routecost', tags=['Цены']
)
main_router.include_router(
    passenger_router,
    prefix='/passenger',
    tags=['Пассажиры'],
)
main_router.include_router(
    ticket_router,
    prefix='/ticket',
    tags=['Билеты'],
)
main_router.include_router(user_router)
