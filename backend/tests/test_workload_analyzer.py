def test_analyze_efficient_workload(client):
    response = client.post(
        "/api/v1/workloads/analyze",
        json={
            "name": "Healthy API",
            "cpu_usage": 65,
            "memory_usage": 60,
            "replicas": 2,
            "runtime_hours": 24,
            "requests_per_day": 50000,
            "workload_type": "realtime",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["efficiency_score"] == 100
    assert data["status"] == "Efficient"
    assert data["recommendations"] == []


def test_detect_over_provisioned_workload(client):
    response = client.post(
        "/api/v1/workloads/analyze",
        json={
            "name": "Batch Worker",
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

    assert data["efficiency_score"] == 60
    assert data["status"] == "Review Recommended"

    codes = [
        recommendation["code"]
        for recommendation
        in data["recommendations"]
    ]

    assert "LOW_CPU_UTILIZATION" in codes
    assert "POSSIBLE_EXCESS_REPLICAS" in codes
    assert "SCHEDULING_OPPORTUNITY" in codes


def test_reject_invalid_cpu_usage(client):
    response = client.post(
        "/api/v1/workloads/analyze",
        json={
            "name": "Invalid Workload",
            "cpu_usage": 150,
            "memory_usage": 50,
            "replicas": 1,
            "runtime_hours": 5,
            "requests_per_day": 100,
            "workload_type": "batch",
        },
    )

    assert response.status_code == 422