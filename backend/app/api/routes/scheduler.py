from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.history import (
    save_carbon_schedule,
)
from app.schemas.scheduler import (
    CarbonScheduleRequest,
    CarbonScheduleResponse,
)
from app.services.carbon.base import (
    CarbonProviderError,
)
from app.services.carbon.gb_provider import (
    GBCarbonIntensityProvider,
)
from app.services.carbon.scheduler import (
    find_best_carbon_window,
)


router = APIRouter(
    prefix="/carbon",
    tags=["Carbon Scheduling"],
)


provider = GBCarbonIntensityProvider()


@router.post(
    "/schedule",
    response_model=CarbonScheduleResponse,
)
async def schedule_workload(
    request: CarbonScheduleRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        forecast = await provider.get_forecast()

        result = find_best_carbon_window(
            workload_name=request.workload_name,
            forecast_points=forecast.points,
            runtime_minutes=(
                request.runtime_minutes
            ),
            max_delay_hours=(
                request.max_delay_hours
            ),
        )

        await save_carbon_schedule(
            db,
            request,
            result,
        )

        return result

    except CarbonProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Carbon data provider "
                "is unavailable."
            ),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc