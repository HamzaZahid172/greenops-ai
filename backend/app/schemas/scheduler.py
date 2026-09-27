from datetime import datetime

from pydantic import BaseModel, Field


class CarbonScheduleRequest(BaseModel):
    workload_name: str = Field(
        min_length=2,
        max_length=100,
    )

    runtime_minutes: int = Field(
        ge=30,
        le=1440,
    )

    max_delay_hours: int = Field(
        ge=1,
        le=24,
    )


class ScheduleWindow(BaseModel):
    start_time: datetime
    end_time: datetime
    average_intensity: float


class CarbonScheduleResponse(BaseModel):
    workload_name: str

    current_window: ScheduleWindow
    recommended_window: ScheduleWindow

    reduction_percent: float

    optimization_available: bool

    message: str