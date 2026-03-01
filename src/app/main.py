from fastapi import FastAPI

from app.api.v1.api import api_router
from app.api.v1.endpoints.health import router as health_router
from app.core.config import CONFIG

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url=f"{CONFIG.api.prefix}/openapi.json",
    docs_url=f"{CONFIG.api.prefix}/docs",
    redoc_url=f"{CONFIG.api.prefix}/redoc",
)

main_app.include_router(router=api_router, prefix=CONFIG.api.prefix)
main_app.include_router(
    router=health_router,
    prefix=f"{CONFIG.api.prefix}/health",
    tags=["API Health"],
)
