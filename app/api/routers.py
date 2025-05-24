from fastapi import APIRouter

from app.api.endpoints.v1 import router as router_v1

main_router = APIRouter()
main_router.include_router(
    router_v1,
    prefix='/v1',
    tags=['v1'],
)
