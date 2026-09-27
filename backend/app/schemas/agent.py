from typing import Any

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.workload import (
    WorkloadType,
)


class AgentWorkloadContext(BaseModel):
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


class AgentQueryRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
    )

    workload: (
        AgentWorkloadContext | None
    ) = None

    runtime_minutes: (
        int | None
    ) = Field(
        default=None,
        ge=30,
        le=1440,
    )

    max_delay_hours: (
        int | None
    ) = Field(
        default=None,
        ge=1,
        le=24,
    )


class AgentToolTrace(BaseModel):
    tool: str

    output: dict[str, Any]


class AgentQueryResponse(BaseModel):
    answer: str

    tools_used: list[str]

    trace: list[AgentToolTrace]

    provider: str