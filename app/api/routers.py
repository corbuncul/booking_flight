from fastapi import APIRouter

from app.api.endpoints.user import router as user_router
from app.api.endpoints.v1.common import router as router_v1

main_router = APIRouter()
main_router.include_router(
    router_v1,
    prefix='/v1',
    tags=['v1'],
)
main_router.include_router(user_router)
