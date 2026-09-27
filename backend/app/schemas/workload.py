from enum import Enum

from pydantic import BaseModel, Field


class WorkloadType(str, Enum):
    realtime = "realtime"
    batch = "batch"
    flexible = "flexible"
    critical = "critical"
    non_critical = "non-critical"


class WorkloadRequest(BaseModel):
    name: str = Field(
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


class Recommendation(BaseModel):
    code: str
    title: str
    message: str
    severity: str
    estimated_saving_percent: int | None = None


class WorkloadAnalysisResponse(BaseModel):
    workload_name: str
    efficiency_score: int
    status: str
    recommendations: list[Recommendation]