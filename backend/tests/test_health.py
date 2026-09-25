def test_health_check(client):
    response = client.get(
        "/api/v1/health",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "GreenOps AI"
    assert data["version"] == "0.1.0"

    # During pytest we intentionally run in test mode.
    assert data["environment"] == "test"


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "Welcome to GreenOps AI"
    )

    assert data["version"] == "0.1.0"