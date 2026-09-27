from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.session import get_db

from app.repositories.history import (
    get_schedule_history,
    get_workload_history,
)

from app.schemas.history import (
    ScheduleHistoryItem,
    WorkloadHistoryItem,
)


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get(
    "/workloads",
    response_model=list[WorkloadHistoryItem],
)
async def workload_history(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    return await get_workload_history(
        db,
        limit,
    )


@router.get(
    "/schedules",
    response_model=list[ScheduleHistoryItem],
)
async def schedule_history(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    return await get_schedule_history(
        db,
        limit,
    )