from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Open-source AI platform for analyzing and optimizing "
        "cloud and AI workloads for cost, performance, "
        "and carbon efficiency."
    ),
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to GreenOps AI",
        "version": settings.app_version,
    }


app.include_router(
    health_router,
    prefix=settings.api_v1_prefix,
)