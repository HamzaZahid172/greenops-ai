from unittest.mock import (
    AsyncMock,
)

from app.services.agent import (
    agent as agent_service,
)


def test_agent_uses_workload_tool(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        agent_service.provider,
        "generate",
        AsyncMock(
            side_effect=[
                (
                    '{"tools": '
                    '["analyze_workload"]}'
                ),
                (
                    "The workload should "
                    "be reviewed because "
                    "GreenOps detected "
                    "underutilization."
                ),
            ],
        ),
    )


    response = client.post(
        "/api/v1/agent/query",
        json={
            "question":
                "Is this workload efficient?",

            "workload": {
                "name":
                    "Embedding Worker",

                "cpu_usage": 15,

                "memory_usage": 50,

                "replicas": 5,

                "runtime_hours": 12,

                "requests_per_day": 1000,

                "workload_type": "batch",
            },

            "runtime_minutes": 120,

            "max_delay_hours": 6,
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        "analyze_workload"
        in data["tools_used"]
    )


    assert (
        len(data["trace"])
        == 1
    )


    assert (
        data["trace"][0]["tool"]
        == "analyze_workload"
    )


def test_agent_fallback_planner(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        agent_service.provider,
        "generate",
        AsyncMock(
            side_effect=[
                "INVALID PLANNER OUTPUT",
                "Grounded final answer.",
            ],
        ),
    )


    response = client.post(
        "/api/v1/agent/query",
        json={
            "question":
                "Is this workload efficient?",

            "workload": {
                "name": "API Worker",

                "cpu_usage": 65,

                "memory_usage": 60,

                "replicas": 2,

                "runtime_hours": 24,

                "requests_per_day": 50000,

                "workload_type":
                    "realtime",
            },
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        "analyze_workload"
        in data["tools_used"]
    )