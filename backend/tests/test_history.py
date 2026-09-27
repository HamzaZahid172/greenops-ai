from datetime import (
    UTC,
    datetime,
    timedelta,
)

from unittest.mock import AsyncMock

from app.api.routes import scheduler

from app.schemas.carbon import (
    CarbonForecastResponse,
    CarbonIntensityPoint,
)


def test_workload_analysis_is_saved_to_history(
    client,
):
    create_response = client.post(
        "/api/v1/workloads/analyze",
        json={
            "name": "History Worker",
            "cpu_usage": 25,
            "memory_usage": 40,
            "replicas": 4,
            "runtime_hours": 8,
            "requests_per_day": 2000,
            "workload_type": "batch",
        },
    )

    assert create_response.status_code == 200

    history_response = client.get(
        "/api/v1/history/workloads?limit=20"
    )

    assert history_response.status_code == 200

    records = history_response.json()

    assert any(
        record["workload_name"]
        == "History Worker"
        for record in records
    )


def test_carbon_schedule_is_saved_to_history(
    client,
    monkeypatch,
):
    start = datetime(
        2026,
        9,
        26,
        0,
        0,
        tzinfo=UTC,
    )

    values = [
        220,
        210,
        170,
        150,
        100,
        90,
    ]

    points = [
        CarbonIntensityPoint(
            from_time=(
                start
                + timedelta(
                    minutes=index * 30
                )
            ),
            to_time=(
                start
                + timedelta(
                    minutes=(index + 1) * 30
                )
            ),
            forecast=value,
            actual=None,
            index="moderate",
        )
        for index, value
        in enumerate(values)
    ]

    forecast = CarbonForecastResponse(
        provider="Test Provider",
        region="Test Region",
        unit="gCO2/kWh",
        points=points,
    )

    monkeypatch.setattr(
        scheduler.provider,
        "get_forecast",
        AsyncMock(
            return_value=forecast
        ),
    )

    create_response = client.post(
        "/api/v1/carbon/schedule",
        json={
            "workload_name":
                "History Carbon Job",

            "runtime_minutes": 60,

            "max_delay_hours": 2,
        },
    )

    assert create_response.status_code == 200

    history_response = client.get(
        "/api/v1/history/schedules?limit=20"
    )

    assert history_response.status_code == 200

    records = history_response.json()

    assert any(
        record["workload_name"]
        == "History Carbon Job"
        for record in records
    )