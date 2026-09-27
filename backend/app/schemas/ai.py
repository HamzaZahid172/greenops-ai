from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.workload import (
    WorkloadType,
)


class AIWorkloadExplanationRequest(BaseModel):

    workload_name: str = Field(
        min_length=2,
        max_length=100,
    )

    cpu_usage: float = Field(
        ge=0,
        le=100,
    )

    memory_usage: float = Field(
        ge=0,
        le=100,
    )

    replicas: int = Field(
        ge=1,
        le=1000,
    )

    runtime_hours: float = Field(
        gt=0,
        le=24,
    )

    requests_per_day: int = Field(
        ge=0,
    )

    workload_type: WorkloadType


class AIExplanationResponse(BaseModel):

    workload_name: str

    efficiency_score: int

    status: str

    explanation: str

    provider: str