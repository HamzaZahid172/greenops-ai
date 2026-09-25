from unittest.mock import AsyncMock

from app.api.routes import ai
from app.services.ai.base import AIProviderError


def test_ai_workload_explanation(
    client,
    monkeypatch,
):

    mock_explanation = (
        "The workload appears "
        "over-provisioned because CPU "
        "utilization is low relative "
        "to the replica count."
    )


    monkeypatch.setattr(
        ai.provider,
        "generate",
        AsyncMock(
            return_value=mock_explanation,
        ),
    )


    response = client.post(
        "/api/v1/ai/explain-workload",
        json={
            "workload_name":
                "Embedding Worker",

            "cpu_usage": 15,

            "memory_usage": 50,

            "replicas": 5,

            "runtime_hours": 12,

            "requests_per_day": 1000,

            "workload_type": "batch",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["workload_name"]
        == "Embedding Worker"
    )

    assert (
        data["efficiency_score"]
        == 60
    )

    assert (
        data["status"]
        == "Review Recommended"
    )

    assert (
        data["explanation"]
        == mock_explanation
    )

    assert (
        data["provider"]
        == "ollama"
    )

def test_ai_provider_unavailable(
    client,
    monkeypatch,
):
    monkeypatch.setattr(
        ai.provider,
        "generate",
        AsyncMock(
            side_effect=AIProviderError(
                "Provider unavailable"
            ),
        ),
    )

    response = client.post(
        "/api/v1/ai/explain-workload",
        json={
            "workload_name": "Embedding Worker",
            "cpu_usage": 15,
            "memory_usage": 50,
            "replicas": 5,
            "runtime_hours": 12,
            "requests_per_day": 1000,
            "workload_type": "batch",
        },
    )

    assert response.status_code == 503

    data = response.json()

    assert (
        data["detail"]
        == "AI provider is currently unavailable."
    )