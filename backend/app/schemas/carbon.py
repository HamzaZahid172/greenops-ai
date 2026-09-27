from datetime import datetime

from pydantic import BaseModel


class CarbonIntensityPoint(BaseModel):
    from_time: datetime
    to_time: datetime

    forecast: int
    actual: int | None = None

    index: str


class CarbonCurrentResponse(BaseModel):
    provider: str
    region: str
    unit: str

    intensity: CarbonIntensityPoint


class CarbonForecastResponse(BaseModel):
    provider: str
    region: str
    unit: str

    points: list[CarbonIntensityPoint]