from app.schemas.workload import (
    WorkloadAnalysisResponse,
    WorkloadRequest,
)
from app.services.workload_analyzer import analyze_workload
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.history import (
    save_workload_analysis,
)


router = APIRouter(
    prefix="/workloads",
    tags=["Workloads"],
)


@router.post(
    "/analyze",
    response_model=WorkloadAnalysisResponse,
)
async def analyze_workload_endpoint(
    workload: WorkloadRequest,
    db: AsyncSession = Depends(get_db),
):
    result = analyze_workload(workload)

    await save_workload_analysis(
        db,
        workload,
        result,
    )

    return result