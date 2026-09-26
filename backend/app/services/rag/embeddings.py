import httpx

from app.core.config import settings
from app.services.ai.base import AIProviderError


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

        try:
            async with httpx.AsyncClient(
                timeout=120.0,
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

            raise AIProviderError(
                "Embedding provider unavailable."
            ) from exc

        embeddings = data.get(
            "embeddings"
        )

        if not embeddings:
            raise AIProviderError(
                "Embedding provider returned "
                "no embeddings."
            )

        for embedding in embeddings:
            if (
                len(embedding)
                != settings.rag_embedding_dimension
            ):
                raise AIProviderError(
                    "Unexpected embedding dimension."
                )

        return embeddings


embedding_provider = (
    OllamaEmbeddingProvider()
)