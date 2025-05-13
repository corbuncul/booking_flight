from fastapi import APIRouter

from app.api.endpoints import (
    city_router,
    flight_router,
    passenger_router,
    route_router,
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
    flight_router,
    prefix='/flight',
    tags=['Рейсы'],
)
main_router.include_router(route_router, prefix='/route', tags=['Маршруты'])
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
