from fastapi import APIRouter

from app.schemas.workload import (
    WorkloadAnalysisResponse,
    WorkloadRequest,
)
from app.services.workload_analyzer import analyze_workload


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
):
    return analyze_workload(workload)