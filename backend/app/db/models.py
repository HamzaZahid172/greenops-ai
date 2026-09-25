from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    func,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


class WorkloadAnalysisRecord(Base):
    __tablename__ = "workload_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    workload_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cpu_usage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    memory_usage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    replicas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    runtime_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    requests_per_day: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    workload_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    efficiency_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    recommendations: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class CarbonScheduleRecord(Base):
    __tablename__ = "carbon_schedules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    workload_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    runtime_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_delay_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    current_start_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    current_end_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    current_average_intensity: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    recommended_start_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    recommended_end_time: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    recommended_average_intensity: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    reduction_percent: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    optimization_available: Mapped[bool] = (
        mapped_column(
            Boolean,
            nullable=False,
        )
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )