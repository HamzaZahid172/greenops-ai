import time

import httpx

from app.core.config import settings

from app.observability.metrics import (
    AI_ERRORS_TOTAL,
    EMBEDDING_DURATION_SECONDS,
)

from app.services.ai.base import (
    AIProviderError,
)


class OllamaEmbeddingProvider:

    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        url = (
            f"{settings.ollama_base_url}"
            "/api/embed"
        )

        payload = {
            "model":
                settings.ollama_embedding_model,
            "input": texts,
        }

        started = time.perf_counter()

        try:
            timeout = httpx.Timeout(
                connect=10.0,
                read=180.0,
                write=60.0,
                pool=10.0,
            )

            async with httpx.AsyncClient(
                timeout=timeout,
            ) as client:

                response = await client.post(
                    url,
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

        except (
            httpx.HTTPError,
            ValueError,
        ) as exc:

            AI_ERRORS_TOTAL.labels(
                provider="ollama",
                operation="embedding",
            ).inc()

            raise AIProviderError(
                "Embedding provider unavailable."
            ) from exc

        finally:
            duration = (
                time.perf_counter()
                - started
            )

            EMBEDDING_DURATION_SECONDS.labels(
                provider="ollama",
                model=(
                    settings
                    .ollama_embedding_model
                ),
            ).observe(duration)

        embeddings = data.get(
            "embeddings"
        )

        if not embeddings:

            AI_ERRORS_TOTAL.labels(
                provider="ollama",
                operation="empty_embedding",
            ).inc()

            raise AIProviderError(
                "Embedding provider returned "
                "no embeddings."
            )

        for embedding in embeddings:

            if (
                len(embedding)
                != settings.rag_embedding_dimension
            ):

                AI_ERRORS_TOTAL.labels(
                    provider="ollama",
                    operation=(
                        "embedding_dimension"
                    ),
                ).inc()

                raise AIProviderError(
                    "Unexpected embedding dimension."
                )

        return embeddings


embedding_provider = (
    OllamaEmbeddingProvider()
)