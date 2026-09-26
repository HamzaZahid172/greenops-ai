from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    func,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base
from pgvector.sqlalchemy import Vector


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

class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = (
        mapped_column(
            Vector(768),
            nullable=False,
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )