from unittest.mock import (
    AsyncMock,
)

from app.services.agent import (
    agent as agent_service,
)

from app.schemas.rag import (
    RAGSearchHit,
)

from app.services.agent import (
    tools as tools_service,
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

def test_agent_uses_documentation_tool(
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
                    '["search_documentation"]}'
                ),
                (
                    "The documentation requires "
                    "at least three replicas."
                ),
            ],
        ),
    )


    monkeypatch.setattr(
        tools_service,
        "search_knowledge_base",
        AsyncMock(
            return_value=[
                RAGSearchHit(
                    document_id=1,
                    filename=(
                        "payment-runbook.md"
                    ),
                    chunk_index=0,
                    content=(
                        "The payment service "
                        "requires at least "
                        "three replicas."
                    ),
                    similarity=0.98,
                )
            ]
        ),
    )


    response = client.post(
        "/api/v1/agent/query",
        json={
            "question": (
                "According to the runbook, "
                "can payment run with "
                "two replicas?"
            )
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert (
        "search_documentation"
        in data["tools_used"]
    )

    assert (
        data["trace"][0]["tool"]
        == "search_documentation"
    )

    assert (
        "three replicas"
        in data["answer"]
    )

def test_agent_filters_inapplicable_workload_tool(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        agent_service.provider,
        "generate",
        AsyncMock(
            side_effect=[
                (
                    '{"tools": ['
                    '"search_documentation", '
                    '"analyze_workload"'
                    ']}'
                ),
                (
                    "The documentation requires "
                    "at least three replicas."
                ),
            ],
        ),
    )


    monkeypatch.setattr(
        tools_service,
        "search_knowledge_base",
        AsyncMock(
            return_value=[
                RAGSearchHit(
                    document_id=1,

                    filename=(
                        "payment-runbook.md"
                    ),

                    chunk_index=0,

                    content=(
                        "The payment service "
                        "requires at least "
                        "three replicas."
                    ),

                    similarity=0.98,
                )
            ]
        ),
    )


    response = client.post(
        "/api/v1/agent/query",
        json={
            "question": (
                "According to the runbook, "
                "can the payment service "
                "run with two replicas?"
            )
        },
    )


    assert response.status_code == 200


    data = response.json()


    # The LLM requested two tools,
    # but analyze_workload is invalid
    # because no workload context exists.
    assert data["tools_used"] == [
        "search_documentation"
    ]


    assert len(
        data["trace"]
    ) == 1


    assert (
        data["trace"][0]["tool"]
        == "search_documentation"
    )


    assert (
        "three replicas"
        in data["answer"]
    )