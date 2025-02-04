from fastapi import APIRouter

from app.api.endpoints import (
    flight_router,
    passenger_router,
    queue_router,
    route_router,
    ticket_router,
    google_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    flight_router,
    prefix='/flight',
    tags=['Рейсы'],
)
main_router.include_router(
    route_router,
    prefix='/route',
    tags=['Маршруты']
)
main_router.include_router(
    passenger_router,
    prefix='/passenger',
    tags=['Пассажиры'],
)
main_router.include_router(
    queue_router,
    prefix='/queue',
    tags=['Очереди'],
)
main_router.include_router(
    ticket_router,
    prefix='/ticket',
    tags=['Билеты'],
)
main_router.include_router(google_router, prefix='/google', tags=['Google'])
main_router.include_router(user_router)
