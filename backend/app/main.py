from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.workloads import router as workloads_router
from app.core.config import settings
from app.api.routes.carbon import (
    router as carbon_router,
)
from app.api.routes.scheduler import (
    router as scheduler_router,
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Open-source AI platform for analyzing and optimizing "
        "cloud and AI workloads for cost, performance, "
        "and carbon efficiency."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(
    workloads_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    carbon_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    scheduler_router,
    prefix=settings.api_v1_prefix,
)