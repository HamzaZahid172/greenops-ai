from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    CarbonScheduleRecord,
    WorkloadAnalysisRecord,
)

from app.schemas.scheduler import (
    CarbonScheduleRequest,
    CarbonScheduleResponse,
)

from app.schemas.workload import (
    WorkloadAnalysisResponse,
    WorkloadRequest,
)


async def save_workload_analysis(
    session: AsyncSession,
    workload: WorkloadRequest,
    analysis: WorkloadAnalysisResponse,
) -> WorkloadAnalysisRecord:

    record = WorkloadAnalysisRecord(
        workload_name=workload.name,
        cpu_usage=workload.cpu_usage,
        memory_usage=workload.memory_usage,
        replicas=workload.replicas,
        runtime_hours=workload.runtime_hours,
        requests_per_day=(
            workload.requests_per_day
        ),
        workload_type=(
            workload.workload_type.value
        ),
        efficiency_score=(
            analysis.efficiency_score
        ),
        status=analysis.status,
        recommendations=[
            item.model_dump()
            for item
            in analysis.recommendations
        ],
    )

    session.add(record)

    await session.commit()
    await session.refresh(record)

    return record


async def save_carbon_schedule(
    session: AsyncSession,
    request: CarbonScheduleRequest,
    result: CarbonScheduleResponse,
) -> CarbonScheduleRecord:

    record = CarbonScheduleRecord(
        workload_name=request.workload_name,
        runtime_minutes=(
            request.runtime_minutes
        ),
        max_delay_hours=(
            request.max_delay_hours
        ),

        current_start_time=(
            result.current_window.start_time
        ),

        current_end_time=(
            result.current_window.end_time
        ),

        current_average_intensity=(
            result
            .current_window
            .average_intensity
        ),

        recommended_start_time=(
            result
            .recommended_window
            .start_time
        ),

        recommended_end_time=(
            result
            .recommended_window
            .end_time
        ),

        recommended_average_intensity=(
            result
            .recommended_window
            .average_intensity
        ),

        reduction_percent=(
            result.reduction_percent
        ),

        optimization_available=(
            result.optimization_available
        ),

        message=result.message,
    )

    session.add(record)

    await session.commit()
    await session.refresh(record)

    return record


async def get_workload_history(
    session: AsyncSession,
    limit: int = 20,
):
    query = (
        select(WorkloadAnalysisRecord)
        .order_by(
            WorkloadAnalysisRecord
            .created_at
            .desc()
        )
        .limit(limit)
    )

    result = await session.execute(query)

    return result.scalars().all()


async def get_schedule_history(
    session: AsyncSession,
    limit: int = 20,
):
    query = (
        select(CarbonScheduleRecord)
        .order_by(
            CarbonScheduleRecord
            .created_at
            .desc()
        )
        .limit(limit)
    )

    result = await session.execute(query)

    return result.scalars().all()