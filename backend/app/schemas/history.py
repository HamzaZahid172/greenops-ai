from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.schemas.workload import Recommendation


class WorkloadHistoryItem(BaseModel):
    id: int

    workload_name: str

    cpu_usage: float
    memory_usage: float

    replicas: int

    runtime_hours: float

    requests_per_day: int

    workload_type: str

    efficiency_score: int

    status: str

    recommendations: list[Recommendation]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScheduleHistoryItem(BaseModel):
    id: int

    workload_name: str

    runtime_minutes: int

    max_delay_hours: int

    current_start_time: datetime
    current_end_time: datetime

    current_average_intensity: float

    recommended_start_time: datetime
    recommended_end_time: datetime

    recommended_average_intensity: float

    reduction_percent: float

    optimization_available: bool

    message: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )