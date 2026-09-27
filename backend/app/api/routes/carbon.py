from fastapi import APIRouter, HTTPException

from app.schemas.carbon import (
    CarbonCurrentResponse,
    CarbonForecastResponse,
)

from app.services.carbon.base import (
    CarbonProviderError,
)

from app.services.carbon.gb_provider import (
    GBCarbonIntensityProvider,
)


router = APIRouter(
    prefix="/carbon",
    tags=["Carbon Intelligence"],
)


provider = GBCarbonIntensityProvider()


@router.get(
    "/current",
    response_model=CarbonCurrentResponse,
)
async def get_current_carbon():
    try:
        return await provider.get_current()

    except CarbonProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail="Carbon data provider unavailable.",
        ) from exc


@router.get(
    "/forecast",
    response_model=CarbonForecastResponse,
)
async def get_carbon_forecast():
    try:
        return await provider.get_forecast()

    except CarbonProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail="Carbon data provider unavailable.",
        ) from exc