from app.db.session import get_db
from app.main import app

def test_health_response_has_request_id(
    client,
):
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    assert (
        "x-request-id"
        in response.headers
    )

    assert response.headers[
        "x-request-id"
    ]


def test_custom_request_id_is_preserved(
    client,
):
    request_id = (
        "greenops-test-request-123"
    )

    response = client.get(
        "/api/v1/health",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "x-request-id"
        ]
        == request_id
    )


def test_metrics_endpoint(
    client,
):
    # Generate at least one HTTP metric.
    health_response = client.get(
        "/api/v1/health"
    )

    assert (
        health_response.status_code
        == 200
    )

    response = client.get(
        "/metrics"
    )

    assert response.status_code == 200

    body = response.text

    assert (
        "greenops_http_requests_total"
        in body
    )

    assert (
        "greenops_http_request_duration_seconds"
        in body
    )

    assert (
        "greenops_ai_generation_duration_seconds"
        in body
    )

    assert (
        "greenops_embedding_duration_seconds"
        in body
    )

    assert (
        "greenops_rag_retrieval_duration_seconds"
        in body
    )

    assert (
        "greenops_agent_tool_duration_seconds"
        in body
    )

    assert (
        "greenops_agent_tool_calls_total"
        in body
    )


def test_readiness_endpoint(
    client,
):
    response = client.get(
        "/api/v1/health/ready"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"
    assert data["database"] == "ready"


def test_readiness_returns_503_when_database_unavailable(
    client,
):

    class BrokenDatabaseSession:

        async def execute(
            self,
            statement,
        ):
            raise RuntimeError(
                "Database unavailable"
            )

    async def broken_get_db():
        yield BrokenDatabaseSession()

    app.dependency_overrides[
        get_db
    ] = broken_get_db

    try:
        response = client.get(
            "/api/v1/health/ready"
        )

        assert response.status_code == 503

        data = response.json()

        assert (
            data["status"]
            == "not_ready"
        )

        assert (
            data["database"]
            == "unavailable"
        )

    finally:
        app.dependency_overrides.clear()