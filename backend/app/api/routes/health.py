from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from sqlalchemy import text

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.config import (
    settings,
)

from app.db.session import (
    get_db,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check():

    return {
        "status": "healthy",
        "application":
            settings.app_name,
        "version":
            settings.app_version,
        "environment":
            settings.app_environment,
    }


@router.get("/ready")
async def readiness_check(
    response: Response,
    db: AsyncSession = Depends(
        get_db
    ),
):

    try:
        await db.execute(
            text("SELECT 1")
        )

        database = "ready"

    except Exception:

        database = "unavailable"

        response.status_code = (
            status
            .HTTP_503_SERVICE_UNAVAILABLE
        )

    overall_status = (
        "ready"
        if database == "ready"
        else "not_ready"
    )

    return {
        "status":
            overall_status,
        "database":
            database,
    }