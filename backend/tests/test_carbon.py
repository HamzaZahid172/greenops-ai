from datetime import UTC, datetime
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.api.routes import carbon
from app.main import app

from app.schemas.carbon import (
    CarbonCurrentResponse,
    CarbonForecastResponse,
    CarbonIntensityPoint,
)


client = TestClient(app)


def build_point(
    forecast: int = 120,
) -> CarbonIntensityPoint:

    return CarbonIntensityPoint(
        from_time=datetime(
            2026,
            9,
            25,
            16,
            0,
            tzinfo=UTC,
        ),
        to_time=datetime(
            2026,
            9,
            25,
            16,
            30,
            tzinfo=UTC,
        ),
        forecast=forecast,
        actual=115,
        index="low",
    )


def test_current_carbon(
    monkeypatch,
):
    response_model = CarbonCurrentResponse(
        provider="Test Provider",
        region="Test Region",
        unit="gCO2/kWh",
        intensity=build_point(),
    )

    monkeypatch.setattr(
        carbon.provider,
        "get_current",
        AsyncMock(
            return_value=response_model,
        ),
    )

    response = client.get(
        "/api/v1/carbon/current",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["provider"] == "Test Provider"
    assert data["region"] == "Test Region"

    assert (
        data["intensity"]["forecast"]
        == 120
    )


def test_carbon_forecast(
    monkeypatch,
):
    response_model = CarbonForecastResponse(
        provider="Test Provider",
        region="Test Region",
        unit="gCO2/kWh",
        points=[
            build_point(120),
            build_point(100),
        ],
    )

    monkeypatch.setattr(
        carbon.provider,
        "get_forecast",
        AsyncMock(
            return_value=response_model,
        ),
    )

    response = client.get(
        "/api/v1/carbon/forecast",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["points"]) == 2