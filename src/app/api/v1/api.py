from fastapi import APIRouter

from app.api.v1.endpoints.prices import router as prices_router

api_router = APIRouter()


api_router.include_router(
    prefix="/v1/articles",
    router=prices_router,
    tags=["prices"],
)
