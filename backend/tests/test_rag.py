from unittest.mock import AsyncMock

from app.api.routes import rag
from app.services.rag.chunker import (
    chunk_text,
)


TEST_VECTOR = (
    [1.0]
    + [0.0] * 767
)


def mock_embeddings(
    monkeypatch,
):
    monkeypatch.setattr(
        rag.embedding_provider,
        "embed_texts",
        AsyncMock(
            side_effect=lambda texts: [
                TEST_VECTOR.copy()
                for _ in texts
            ]
        ),
    )


def test_chunk_text_with_overlap():
    chunks = chunk_text(
        "one two three four five six seven eight",
        chunk_words=4,
        overlap_words=1,
    )

    assert chunks == [
        "one two three four",
        "four five six seven",
        "seven eight",
    ]


def test_reject_unsupported_document(
    client,
):
    response = client.post(
        "/api/v1/rag/documents",
        files={
            "file": (
                "malware.exe",
                b"not a supported document",
                "application/octet-stream",
            )
        },
    )

    assert response.status_code == 400

    assert (
        "Unsupported document type"
        in response.json()["detail"]
    )


def test_upload_search_and_delete_document(
    client,
    monkeypatch,
):
    mock_embeddings(
        monkeypatch
    )

    upload_response = client.post(
        "/api/v1/rag/documents",
        files={
            "file": (
                "phase10-runbook.md",
                (
                    b"# Service Runbook\n"
                    b"The payment service requires "
                    b"at least three replicas."
                ),
                "text/markdown",
            )
        },
    )

    assert upload_response.status_code == 201

    document = (
        upload_response.json()
    )

    document_id = document["id"]

    assert (
        document["filename"]
        == "phase10-runbook.md"
    )

    assert (
        document["chunk_count"]
        >= 1
    )


    list_response = client.get(
        "/api/v1/rag/documents"
    )

    assert list_response.status_code == 200

    documents = list_response.json()

    assert any(
        item["id"] == document_id
        for item in documents
    )


    search_response = client.post(
        "/api/v1/rag/search",
        json={
            "query":
                "minimum replica count",

            "top_k": 10,
        },
    )

    assert search_response.status_code == 200

    search_data = (
        search_response.json()
    )

    assert any(
        result["filename"]
        == "phase10-runbook.md"
        for result
        in search_data["results"]
    )


    delete_response = client.delete(
        f"/api/v1/rag/documents/{document_id}"
    )

    assert delete_response.status_code == 204


    list_after_delete = client.get(
        "/api/v1/rag/documents"
    )

    assert all(
        item["id"] != document_id
        for item
        in list_after_delete.json()
    )


def test_rag_answer_uses_retrieved_source(
    client,
    monkeypatch,
):
    mock_embeddings(
        monkeypatch
    )

    monkeypatch.setattr(
        rag.ai_provider,
        "generate",
        AsyncMock(
            return_value=(
                "The payment service must "
                "maintain at least three replicas."
            )
        ),
    )


    upload_response = client.post(
        "/api/v1/rag/documents",
        files={
            "file": (
                "payment-policy.md",
                (
                    b"# Payment Policy\n"
                    b"The payment service must "
                    b"maintain a minimum of "
                    b"three replicas."
                ),
                "text/markdown",
            )
        },
    )

    assert upload_response.status_code == 201

    document_id = (
        upload_response.json()["id"]
    )


    response = client.post(
        "/api/v1/rag/ask",
        json={
            "question":
                "Can the payment service "
                "run with two replicas?",

            "top_k": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "three replicas"
        in data["answer"]
    )

    assert any(
        source["filename"]
        == "payment-policy.md"
        for source
        in data["sources"]
    )


    cleanup = client.delete(
        f"/api/v1/rag/documents/{document_id}"
    )

    assert cleanup.status_code == 204